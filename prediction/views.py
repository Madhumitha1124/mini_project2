from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import numpy as np
import pickle
import os
import pandas as pd
import json

from .utils import get_weather_for_city, get_market_data_for_crop
from .soil_api import get_soil_data, fetch_soilgrids_data, get_coordinates_from_location

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

model = pickle.load(open(os.path.join(BASE_DIR, "crop_model.pkl"), "rb"))

# Crop name mapping - maps numeric predictions to crop names
CROP_NAMES = {
    0: "Rice",
    1: "Maize",
    2: "Chickpea",
    3: "Kidney Beans",
    4: "Pigeon Peas",
    5: "Moth Beans",
    6: "Mung Bean",
    7: "Black Gram",
    8: "Lentil",
    9: "Pomegranate",
    10: "Banana",
    11: "Mango",
    12: "Grapes",
    13: "Watermelon",
    14: "Muskmelon",
    15: "Apple",
    16: "Orange",
    17: "Papaya",
    18: "Coconut",
    19: "Cotton",
    20: "Sugarcane",
    21: "Tobacco",
}

CROP_DISEASES = {
    "Rice": {
        "disease": "Blast",
        "solution": "Use resistant varieties, avoid excess nitrogen, and spray Tricyclazole at early symptom stage."
    },
    "Wheat": {
        "disease": "Rust",
        "solution": "Use rust-tolerant seeds, monitor fields regularly, and apply Propiconazole when infection appears."
    },
    "Maize": {
        "disease": "Leaf Blight",
        "solution": "Remove infected residue, rotate crops, and spray Mancozeb at recommended dose."
    },
    "Cotton": {
        "disease": "Bacterial Blight",
        "solution": "Use certified seed, avoid overhead irrigation, and spray Copper oxychloride for disease control."
    },
    "Sugarcane": {
        "disease": "Red Rot",
        "solution": "Plant disease-free setts, treat setts before sowing, and remove infected clumps immediately."
    },
    "Banana": {
        "disease": "Panama Wilt",
        "solution": "Use wilt-resistant varieties, ensure good drainage, and drench soil with Trichoderma-based biofungicide."
    },
    "Groundnut": {
        "disease": "Tikka Leaf Spot",
        "solution": "Follow crop rotation, maintain spacing, and spray Chlorothalonil at first appearance."
    },
    "Sorghum": {
        "disease": "Anthracnose",
        "solution": "Use tolerant cultivars, remove infected plant debris, and apply Carbendazim as per guidelines."
    },
    "Pulses": {
        "disease": "Wilt",
        "solution": "Treat seeds with biofungicide, improve field drainage, and avoid continuous pulse cultivation in same plot."
    },
    "Vegetables": {
        "disease": "Powdery Mildew",
        "solution": "Improve airflow, avoid excessive humidity, and spray wettable sulfur when symptoms start."
    },
}

CROP_VARIETY_SUGGESTIONS = {
    "Vegetables": ["Tomato", "Brinjal", "Chilli", "Okra", "Cabbage", "Cauliflower"],
    "Pulses": ["Green Gram", "Black Gram", "Pigeon Pea", "Chickpea", "Lentil"],
}


def get_crop_disease_info(crop_name):
    info = CROP_DISEASES.get(crop_name)
    if info:
        return info
    return {
        "disease": "No major disease data available",
        "solution": "Follow integrated pest and disease management: field scouting, crop rotation, certified seeds, and local agronomy advice."
    }


def get_crop_suggestions(crop_name):
    return CROP_VARIETY_SUGGESTIONS.get((crop_name or "").strip(), [])

# Prepare dataset-based centroids for each crop to improve matching
DATA_CSV_PATH = os.path.join(os.path.dirname(BASE_DIR), 'Soil_Based_Crop_Recommendations.csv')
CROP_CENTROIDS = {}
CROP_STD = {'N': 1.0, 'P': 1.0, 'K': 1.0, 'pH': 0.1, 'OC': 0.01}
try:
    if os.path.exists(DATA_CSV_PATH):
        _df_cent = pd.read_csv(DATA_CSV_PATH)
        if 'Top_Recommended_Crop' in _df_cent.columns:
            grp = _df_cent.groupby('Top_Recommended_Crop')
            for crop_name, g in grp:
                CROP_CENTROIDS[crop_name] = {
                    'N': float(g['Nitrogen (kg/ha)'].mean()),
                    'P': float(g['Phosphorus (kg/ha)'].mean()),
                    'K': float(g['Potassium (kg/ha)'].mean()),
                    'pH': float(g['pH'].mean()) if 'pH' in g.columns else None,
                    'OC': float(g['Organic Carbon (%)'].mean()) if 'Organic Carbon (%)' in g.columns else None,
                }
            # dataset-wide std for normalization
            CROP_STD['N'] = float(_df_cent['Nitrogen (kg/ha)'].std() or 1.0)
            CROP_STD['P'] = float(_df_cent['Phosphorus (kg/ha)'].std() or 1.0)
            CROP_STD['K'] = float(_df_cent['Potassium (kg/ha)'].std() or 1.0)
            if 'pH' in _df_cent.columns:
                CROP_STD['pH'] = float(_df_cent['pH'].std() or 0.1)
            if 'Organic Carbon (%)' in _df_cent.columns:
                CROP_STD['OC'] = float(_df_cent['Organic Carbon (%)'].std() or 0.01)
except Exception:
    # If anything fails, fall back to defaults defined above
    CROP_CENTROIDS = {}


def get_crop_from_soil_data(nitrogen, phosphorus, potassium, ph, oc, temperature=None, humidity=None, rainfall=None):
    """
    Recommend crop using a combined score:
    - Range-based soft matching (captures acceptable parameter windows)
    - Distance to dataset centroid (more discriminative)
    - Climate compatibility (temperature, humidity, rainfall)

    Returns (best_crop_name, confidence_score_0_100)
    """
    # Define comprehensive crop ranges with climate preferences
    crop_ranges = {
        "Rice": {
            "pH": (4.50, 8.49), "N": (150, 600), "P": (10, 120), "K": (80, 398),
            "Temp": (20, 30), "Humidity": (60, 90), "Rainfall": (100, 300)
        },
        "Wheat": {
            "pH": (5.5, 8.5), "N": (100, 200), "P": (20, 60), "K": (60, 150),
            "Temp": (10, 25), "Humidity": (50, 70), "Rainfall": (40, 100)
        },
        "Maize": {
            "pH": (5.5, 7.5), "N": (150, 300), "P": (40, 80), "K": (80, 150),
            "Temp": (21, 37), "Humidity": (60, 80), "Rainfall": (50, 150)
        },
        "Cotton": {
            "pH": (7.28, 8.47), "N": (196, 578), "P": (10, 118), "K": (84, 395),
            "Temp": (21, 30), "Humidity": (50, 70), "Rainfall": (50, 100)
        },
        "Sugarcane": {
            "pH": (8.34, 8.43), "N": (356, 569), "P": (23, 46), "K": (167, 382),
            "Temp": (21, 27), "Humidity": (70, 85), "Rainfall": (150, 250)
        },
        "Banana": {
            "pH": (5.09, 5.21), "N": (270, 487), "P": (11, 73), "K": (94, 309),
            "Temp": (15, 35), "Humidity": (75, 90), "Rainfall": (150, 225)
        },
        "Groundnut": {
            "pH": (4.56, 7.55), "N": (154, 595), "P": (10, 120), "K": (80, 387),
            "Temp": (24, 30), "Humidity": (60, 75), "Rainfall": (50, 100)
        },
        "Sorghum": {
            "pH": (4.53, 8.49), "N": (243, 572), "P": (10, 102), "K": (176, 366),
            "Temp": (21, 37), "Humidity": (50, 70), "Rainfall": (40, 100)
        },
        "Pulses": {
            "pH": (5.5, 8.0), "N": (50, 100), "P": (20, 50), "K": (60, 150),
            "Temp": (15, 28), "Humidity": (50, 70), "Rainfall": (40, 80)
        },
        "Vegetables": {
            "pH": (5.5, 7.5), "N": (200, 400), "P": (50, 100), "K": (150, 300),
            "Temp": (15, 30), "Humidity": (60, 80), "Rainfall": (50, 150)
        },
    }

    best_crop = None
    best_score = -1.0

    for crop, ranges in crop_ranges.items():
        # Soil-based score (0-100)
        soil_score = 0.0
        soil_max = 4.0

        # pH score
        ph_min, ph_max = ranges['pH']
        if ph_min <= ph <= ph_max:
            soil_score += 1.0
        elif ph_min - 0.5 <= ph <= ph_max + 0.5:
            soil_score += 0.5

        # Nitrogen score
        n_min, n_max = ranges['N']
        if n_min <= nitrogen <= n_max:
            soil_score += 1.0
        elif n_min - 50 <= nitrogen <= n_max + 50:
            soil_score += 0.5

        # Phosphorus score
        p_min, p_max = ranges['P']
        if p_min <= phosphorus <= p_max:
            soil_score += 1.0
        elif p_min - 10 <= phosphorus <= p_max + 10:
            soil_score += 0.5

        # Potassium score
        k_min, k_max = ranges['K']
        if k_min <= potassium <= k_max:
            soil_score += 1.0
        elif k_min - 20 <= potassium <= k_max + 20:
            soil_score += 0.5

        soil_score_normalized = (soil_score / soil_max) * 100.0

        # Climate score (if climate data is provided)
        climate_score = 50.0  # Default neutral
        climate_subscore = 0.0
        climate_max = 3.0  # Now includes rainfall
        
        if temperature is not None and humidity is not None:
            # Temperature score
            temp_min, temp_max = ranges['Temp']
            if temp_min <= temperature <= temp_max:
                climate_subscore += 1.0
            elif temp_min - 2 <= temperature <= temp_max + 2:
                climate_subscore += 0.5
            
            # Humidity score
            hum_min, hum_max = ranges['Humidity']
            if hum_min <= humidity <= hum_max:
                climate_subscore += 1.0
            elif hum_min - 5 <= humidity <= hum_max + 5:
                climate_subscore += 0.5
            
            climate_score = (climate_subscore / 2.0) * 100.0
        
        # Rainfall score (if provided)
        if rainfall is not None and rainfall > 0:
            rain_min, rain_max = ranges['Rainfall']
            if rain_min <= rainfall <= rain_max:
                climate_subscore += 1.0
            elif rain_min - 50 <= rainfall <= rain_max + 50:
                climate_subscore += 0.5
            
            climate_score = (climate_subscore / climate_max) * 100.0

        # Distance-based score using dataset centroid
        distance_score = 50.0  # Default neutral
        if crop.title() in CROP_CENTROIDS:
            centroid = CROP_CENTROIDS[crop.title()]
            diffs = []
            try:
                diffs.append(((nitrogen - centroid['N']) / max(CROP_STD['N'], 1e-6)) ** 2)
                diffs.append(((phosphorus - centroid['P']) / max(CROP_STD['P'], 1e-6)) ** 2)
                diffs.append(((potassium - centroid['K']) / max(CROP_STD['K'], 1e-6)) ** 2)
                if centroid.get('pH'):
                    diffs.append(((ph - centroid['pH']) / max(CROP_STD['pH'], 1e-6)) ** 2)
                normalized_dist = float(np.sqrt(sum(diffs)))
                distance_score = 100.0 * (1.0 / (1.0 + normalized_dist))
            except Exception:
                distance_score = 50.0

        # Combine scores: soil (50%), climate (30%), dataset similarity (20%)
        final_score = 0.50 * soil_score_normalized + 0.30 * climate_score + 0.20 * distance_score

        if final_score > best_score:
            best_score = final_score
            best_crop = crop

    if best_crop is None:
        return "Rice", 0.0

    return best_crop, round(float(best_score), 2)


def index(request):
    return render(request, "index.html")


def predict(request):
    if request.method == "POST":
        try:
            # Required soil nutrient inputs (model needs N,P,K)
            N = float(request.POST.get('Nitrogen', 0))
            P = float(request.POST.get('Phosphorus', 0))
            K = float(request.POST.get('Potassium', 0))
            ph = float(request.POST.get('pH', 6.5))
            oc = float(request.POST.get('Organic_Carbon', 0.8))

            # Temperature / Humidity can be autofilled from weather API
            temp_raw = request.POST.get('Temperature', '').strip()
            hum_raw = request.POST.get('Humidity', '').strip()
            rain_raw = request.POST.get('Rainfall', '').strip()
            city = request.POST.get('city', '').strip()

            temp = None
            hum = None
            rain = None

            if temp_raw:
                try:
                    temp = float(temp_raw)
                except ValueError:
                    temp = None

            if hum_raw:
                try:
                    hum = float(hum_raw)
                except ValueError:
                    hum = None

            if rain_raw:
                try:
                    rain = float(rain_raw)
                except ValueError:
                    rain = None

            # If temperature or humidity missing and a city is provided, try weather API
            if (temp is None or hum is None) and city:
                w = get_weather_for_city(city)
                if w:
                    if temp is None:
                        temp = w.get('temp')
                    if hum is None:
                        hum = w.get('humidity')
                    if rain is None:
                        rain = w.get('rain')

            # Use intelligent recommendation logic instead of ML model
            # This uses the improved get_crop_from_soil_data function
            crop_name, confidence_score = get_crop_from_soil_data(
                nitrogen=N,
                phosphorus=P,
                potassium=K,
                ph=ph,
                oc=oc,
                temperature=temp,
                humidity=hum,
                rainfall=rain
            )

            market_data = get_market_data_for_crop(crop_name)

            # Indicate whether weather was autofilled
            used_weather = bool(city and (not temp_raw or not hum_raw))

            return render(request, "result.html", {
                "crop": crop_name, 
                "confidence": confidence_score,
                "crop_disease_info": get_crop_disease_info(crop_name),
                "crop_suggestions": get_crop_suggestions(crop_name),
                "market_data": market_data,
                "used_weather": used_weather,
                "nitrogen": N,
                "phosphorus": P,
                "potassium": K,
                "ph": ph,
                "temperature": temp,
                "humidity": hum,
                "rainfall": rain
            })
        except Exception as e:
            return render(request, "index.html", {"error": str(e)})


def soil_analysis(request):
    """Display soil-based crop recommendations"""
    try:
        # Load recommendations CSV
        csv_path = os.path.join(os.path.dirname(BASE_DIR), 
                               'Soil_Based_Crop_Recommendations.csv')
        
        if not os.path.exists(csv_path):
            return render(request, "soil_analysis.html", {
                "error": "Recommendations data not available. Please run the analysis first.",
                "recommendations": []
            })
        
        recommendations = pd.read_csv(csv_path)
        
        # Create properly renamed columns for template
        recommendations_display = recommendations.copy()
        
        # Map original column names to template-friendly names
        column_mapping = {
            'District': 'District',
            'Block': 'Block',
            'pH': 'pH',
            'Organic Carbon (%)': 'Organic_Carbon',
            'EC (dS/m)': 'EC',
            'Nitrogen (kg/ha)': 'Nitrogen_kg_per_ha',
            'Phosphorus (kg/ha)': 'Phosphorus_kg_per_ha',
            'Potassium (kg/ha)': 'Potassium_kg_per_ha',
            'Top_Recommended_Crop': 'Top_Recommended_Crop',
            'Recommendation_Score': 'Recommendation_Score',
            'Fertility_Class': 'Fertility_Class'
        }
        
        # Rename columns
        recommendations_display.rename(columns=column_mapping, inplace=True)
        
        # Convert to list of dictionaries for template
        recommendations_data = recommendations_display.to_dict('records')
        
        # Get statistics
        stats = {
            'total_samples': len(recommendations),
            'avg_score': recommendations['Recommendation_Score'].mean(),
            'high_confidence': len(recommendations[recommendations['Recommendation_Score'] > 85]),
            'most_recommended': recommendations['Top_Recommended_Crop'].value_counts().index[0],
        }
        
        # Get crop distribution
        crop_dist = recommendations['Top_Recommended_Crop'].value_counts().to_dict()
        
        context = {
            'recommendations': recommendations_data,
            'stats': stats,
            'crop_distribution': crop_dist,
            'total_crops': len(crop_dist)
        }
        
        return render(request, "soil_analysis.html", context)
    except Exception as e:
        return render(request, "soil_analysis.html", {
            "error": f"Error loading recommendations: {str(e)}",
            "recommendations": []
        })


def soil_recommendation_api(request):
    """API endpoint for soil-based recommendations with filtering"""
    try:
        csv_path = os.path.join(os.path.dirname(BASE_DIR), 
                               'Soil_Based_Crop_Recommendations.csv')
        
        if not os.path.exists(csv_path):
            return JsonResponse({"error": "Data not available"}, status=404)
        
        recommendations = pd.read_csv(csv_path)
        
        # Create properly renamed columns for API
        column_mapping = {
            'District': 'District',
            'Block': 'Block',
            'pH': 'pH',
            'Organic Carbon (%)': 'Organic_Carbon',
            'EC (dS/m)': 'EC',
            'Nitrogen (kg/ha)': 'Nitrogen_kg_per_ha',
            'Phosphorus (kg/ha)': 'Phosphorus_kg_per_ha',
            'Potassium (kg/ha)': 'Potassium_kg_per_ha',
            'Top_Recommended_Crop': 'Top_Recommended_Crop',
            'Recommendation_Score': 'Recommendation_Score',
            'Fertility_Class': 'Fertility_Class'
        }
        
        recommendations.rename(columns=column_mapping, inplace=True)
        
        # Filter by crop if provided
        crop_filter = request.GET.get('crop', '')
        if crop_filter:
            recommendations = recommendations[recommendations['Top_Recommended_Crop'] == crop_filter]
        
        # Filter by score range
        min_score = float(request.GET.get('min_score', 0))
        max_score = float(request.GET.get('max_score', 100))
        recommendations = recommendations[
            (recommendations['Recommendation_Score'] >= min_score) & 
            (recommendations['Recommendation_Score'] <= max_score)
        ]
        
        # Pagination
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 50))
        total = len(recommendations)
        start = (page - 1) * page_size
        end = start + page_size
        
        recommendations_page = recommendations.iloc[start:end].to_dict('records')
        
        return JsonResponse({
            'data': recommendations_page,
            'total': total,
            'page': page,
            'page_size': page_size,
            'total_pages': (total + page_size - 1) // page_size
        })
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
def advanced_soil_analysis(request):
    """
    Advanced Soil Analysis using SoilGrids API or manual soil parameters
    Users can input location (lat/long or district name) or enter soil values directly
    """
    if request.method == "GET":
        return render(request, "advanced_soil_analysis.html")
    
    if request.method == "POST":
        try:
            def to_float(value, default=0.0):
                """Safely convert form values to float, handling blanks."""
                if value is None:
                    return default
                if isinstance(value, str):
                    value = value.strip()
                    if value == "":
                        return default
                try:
                    return float(value)
                except (TypeError, ValueError):
                    return default

            # Check if this is manual input
            manual_input = request.POST.get("manual_input", "false") == "true"
            
            if manual_input:
                # Process manual soil parameters directly
                N = to_float(request.POST.get("nitrogen"), 0.0)
                P = to_float(request.POST.get("phosphorus"), 0.0)
                K = to_float(request.POST.get("potassium"), 0.0)
                ph = to_float(request.POST.get("ph"), 6.5)
                oc = to_float(request.POST.get("oc"), 0.8)
                cec = to_float(request.POST.get("cec"), 12.0)
                location_name = ""
            else:
                # Process location-based input
                location_name = request.POST.get("location_name", "").strip()
                latitude = request.POST.get("latitude", "").strip()
                longitude = request.POST.get("longitude", "").strip()
                
                # Convert to float if provided
                lat = None
                lon = None
                
                if latitude:
                    try:
                        lat = float(latitude)
                    except ValueError:
                        pass
                
                if longitude:
                    try:
                        lon = float(longitude)
                    except ValueError:
                        pass
                
                # Get soil data
                soil_data = get_soil_data(location_name, lat, lon)
                
                if "error" in soil_data:
                    return JsonResponse(soil_data, status=400)
                
                # Prepare data for crop prediction
                N = to_float(soil_data.get("Nitrogen"), 0.0)
                P = to_float(soil_data.get("Phosphorus"), 0.0)
                K = to_float(soil_data.get("Potassium"), 0.0)
                ph = to_float(soil_data.get("pH"), 6.5)
                oc = to_float(soil_data.get("Organic_Carbon"), 0.8)
                cec = to_float(soil_data.get("CEC"), 12.0)
            
            # Fetch weather data for the location to improve recommendations
            temperature = None
            humidity = None
            rainfall = to_float(request.POST.get("rainfall"), 0.0)
            
            if location_name:
                weather_data = get_weather_for_city(location_name)
                if weather_data:
                    temperature = weather_data.get("temp")
                    humidity = weather_data.get("humidity")
                    if not rainfall or rainfall == 0:
                        rainfall = weather_data.get("rain", 0)
            
            # Get crop recommendation using improved region-aware logic with climate data
            crop_name, confidence_score = get_crop_from_soil_data(
                nitrogen=N, 
                phosphorus=P, 
                potassium=K, 
                ph=ph, 
                oc=oc,
                temperature=temperature,
                humidity=humidity,
                rainfall=rainfall
            )
            
            # Fetch actual N, P, K values from dataset for the recommended crop
            csv_path = os.path.join(os.path.dirname(BASE_DIR), 'Soil_Based_Crop_Recommendations.csv')
            dataset_npk = {"Nitrogen": N, "Phosphorus": P, "Potassium": K}
            
            if os.path.exists(csv_path):
                try:
                    recommendations_df = pd.read_csv(csv_path)
                    crop_data = recommendations_df[recommendations_df['Top_Recommended_Crop'] == crop_name]
                    
                    if not crop_data.empty:
                        # Get average N, P, K values for this crop from dataset
                        dataset_npk = {
                            "Nitrogen": round(crop_data['Nitrogen (kg/ha)'].mean(), 2),
                            "Phosphorus": round(crop_data['Phosphorus (kg/ha)'].mean(), 2),
                            "Potassium": round(crop_data['Potassium (kg/ha)'].mean(), 2)
                        }
                except Exception as e:
                    pass  # Fall back to current values if CSV reading fails
            
            response_data = {
                "success": True,
                "location": location_name or f"{lat}, {lon}" if not manual_input else "Manual Input",
                "soil_parameters": {
                    "Nitrogen": dataset_npk.get("Nitrogen", round(N, 2)),
                    "Phosphorus": dataset_npk.get("Phosphorus", round(P, 2)),
                    "Potassium": dataset_npk.get("Potassium", round(K, 2)),
                    "pH": round(ph, 2),
                    "Organic_Carbon": round(oc, 2),
                    "CEC": round(cec, 2)
                },
                "recommended_crop": crop_name,
                "crop_suggestions": get_crop_suggestions(crop_name),
                "confidence_score": round(confidence_score, 2),
                "disease_info": get_crop_disease_info(crop_name),
                "market_data": get_market_data_for_crop(crop_name)
            }
            
            return JsonResponse(response_data)
        
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
def get_weather_api(request):
    """
    API endpoint to fetch weather data for a given city.
    GET parameter: city (e.g., /api/weather/?city=Delhi)
    Returns: {temperature, humidity, rainfall} or error
    """
    if request.method != 'GET':
        return JsonResponse({"error": "Only GET requests are supported"}, status=405)
    
    city = request.GET.get('city', '').strip()
    
    if not city:
        return JsonResponse({"error": "City parameter is required"}, status=400)
    
    # Call the weather function from utils
    weather_data = get_weather_for_city(city)
    
    if weather_data is None:
        return JsonResponse({
            "error": f"Could not fetch weather data for '{city}'. Please check the city name or configure WEATHER_API_KEY.",
            "city": city
        }, status=404)
    
    return JsonResponse({
        "city": city,
        "temperature": weather_data.get("temp"),
        "humidity": weather_data.get("humidity"),
        "rainfall": weather_data.get("rain", 0),
        "success": True
    })


@csrf_exempt
def get_market_data_api(request):
    """
    API endpoint to fetch market data for a crop.
    GET parameter: crop (e.g., /api/market-data/?crop=Rice)
    """
    if request.method != 'GET':
        return JsonResponse({"error": "Only GET requests are supported"}, status=405)

    crop = request.GET.get('crop', '').strip()
    if not crop:
        return JsonResponse({"error": "crop parameter is required"}, status=400)

    market_data = get_market_data_for_crop(crop)
    return JsonResponse({
        "success": True,
        "market_data": market_data
    })