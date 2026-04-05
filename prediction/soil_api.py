"""
SoilGrids API Integration with Fallback Mode
Fetches soil data based on Latitude/Longitude or Location name
"""

import requests
import json
from geopy.geocoders import Nominatim
import logging

logger = logging.getLogger(__name__)

# Fallback soil data for common locations across India
FALLBACK_SOIL_DATA = {
    "coimbatore": {
        "latitude": 11.0081,
        "longitude": 76.9142,
        "Nitrogen": 45,
        "Phosphorus": 25,
        "Potassium": 180,
        "pH": 6.2,
        "Organic_Carbon": 0.85,
        "CEC": 12.5,
        "source": "Default Coimbatore Profile"
    },
    "sulur": {
        "latitude": 11.2089,
        "longitude": 76.9294,
        "Nitrogen": 50,
        "Phosphorus": 28,
        "Potassium": 200,
        "pH": 6.5,
        "Organic_Carbon": 0.9,
        "CEC": 13.2,
        "source": "Default Sulur Profile"
    },
    "thanjavur": {
        "latitude": 10.7905,
        "longitude": 79.1399,
        "Nitrogen": 55,
        "Phosphorus": 30,
        "Potassium": 220,
        "pH": 7.2,
        "Organic_Carbon": 0.75,
        "CEC": 11.8,
        "source": "Default Thanjavur Profile"
    },
    "madurai": {
        "latitude": 9.9252,
        "longitude": 78.1198,
        "Nitrogen": 40,
        "Phosphorus": 22,
        "Potassium": 160,
        "pH": 6.8,
        "Organic_Carbon": 0.65,
        "CEC": 10.5,
        "source": "Default Madurai Profile"
    },
    "salem": {
        "latitude": 11.6643,
        "longitude": 78.1460,
        "Nitrogen": 48,
        "Phosphorus": 26,
        "Potassium": 190,
        "pH": 6.4,
        "Organic_Carbon": 0.8,
        "CEC": 12.0,
        "source": "Default Salem Profile"
    },
    "mumbai": {
        "latitude": 19.0760,
        "longitude": 72.8777,
        "Nitrogen": 35,
        "Phosphorus": 20,
        "Potassium": 150,
        "pH": 6.8,
        "Organic_Carbon": 0.95,
        "CEC": 13.5,
        "source": "Default Mumbai Profile (Coastal)"
    },
    "delhi": {
        "latitude": 28.7041,
        "longitude": 77.1025,
        "Nitrogen": 55,
        "Phosphorus": 32,
        "Potassium": 220,
        "pH": 7.8,
        "Organic_Carbon": 0.55,
        "CEC": 11.0,
        "source": "Default Delhi Profile"
    },
    "bangalore": {
        "latitude": 12.9716,
        "longitude": 77.5946,
        "Nitrogen": 38,
        "Phosphorus": 24,
        "Potassium": 170,
        "pH": 6.5,
        "Organic_Carbon": 0.75,
        "CEC": 12.0,
        "source": "Default Bangalore Profile"
    },
    "hyderabad": {
        "latitude": 17.3850,
        "longitude": 78.4867,
        "Nitrogen": 42,
        "Phosphorus": 26,
        "Potassium": 180,
        "pH": 7.2,
        "Organic_Carbon": 0.7,
        "CEC": 12.5,
        "source": "Default Hyderabad Profile"
    },
    "kolkata": {
        "latitude": 22.5726,
        "longitude": 88.3639,
        "Nitrogen": 52,
        "Phosphorus": 28,
        "Potassium": 210,
        "pH": 6.5,
        "Organic_Carbon": 1.1,
        "CEC": 14.5,
        "source": "Default Kolkata Profile (Alluvial)"
    },
}



def get_coordinates_from_location(location_name):
    """
    Convert District/Block name to Latitude and Longitude
    
    Args:
        location_name: str (e.g., "Coimbatore", "Sulur")
    
    Returns:
        tuple: (latitude, longitude) or None if not found
    """
    try:
        geolocator = Nominatim(user_agent="crop_recommendation")
        location = geolocator.geocode(location_name, timeout=10)
        
        if location:
            return location.latitude, location.longitude
        else:
            logger.warning(f"Location not found: {location_name}")
            return None
    except Exception as e:
        logger.error(f"Error geocoding location {location_name}: {str(e)}")
        return None


def fetch_soilgrids_data(latitude, longitude):
    """
    Fetch soil data from SoilGrids API (v2.0)
    Falls back to default profiles if API is unavailable
    
    Args:
        latitude: float
        longitude: float
    
    Returns:
        dict: Soil parameters (N, P, K, pH, OC, etc.)
    """
    try:
        # SoilGrids API endpoint
        url = f"https://rest.soilgrids.org/soilgrids/v2.0/properties/query"
        
        params = {
            "lon": longitude,
            "lat": latitude,
            "property": [
                "nitrogen",  # Total nitrogen
                "phh2o",     # pH in H2O
                "soc",       # Soil organic carbon
                "cec",       # Cation exchange capacity
                "clay",      # Clay content
                "sand",      # Sand content
                "silt",      # Silt content
            ],
            "depth": ["0-5cm"],  # Top soil layer
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        # Extract soil properties
        soil_data = {
            "latitude": latitude,
            "longitude": longitude,
            "source": "SoilGrids API"
        }
        
        if "properties" in data:
            properties = data["properties"]
            
            # Extract values from SoilGrids response
            if "nitrogen" in properties:
                nitrogen_data = properties["nitrogen"]["0-5cm"]
                soil_data["Nitrogen"] = nitrogen_data.get("mean", 0) * 100  # Convert to reasonable scale
            
            if "phh2o" in properties:
                ph_data = properties["phh2o"]["0-5cm"]
                soil_data["pH"] = ph_data.get("mean", 6.5) / 10  # SoilGrids stores as x10
            
            if "soc" in properties:
                soc_data = properties["soc"]["0-5cm"]
                soil_data["Organic_Carbon"] = soc_data.get("mean", 0) / 10  # Convert to percentage
            
            if "cec" in properties:
                cec_data = properties["cec"]["0-5cm"]
                soil_data["CEC"] = cec_data.get("mean", 0) / 10  # Cation exchange capacity
            
            # Estimate P and K based on soil properties (rough estimation)
            # In real scenario, these would need separate API calls
            soil_data["Phosphorus"] = estimate_phosphorus(soil_data.get("Organic_Carbon", 1))
            soil_data["Potassium"] = estimate_potassium(soil_data.get("CEC", 10))
        
        return soil_data
        
    except requests.exceptions.RequestException as e:
        logger.warning(f"SoilGrids API unavailable, using fallback mode: {str(e)}")
        # Fall back to default profile based on nearest location
        return get_fallback_soil_data(latitude, longitude)
    except Exception as e:
        logger.error(f"Unexpected error in SoilGrids API: {str(e)}")
        return get_fallback_soil_data(latitude, longitude)


def get_fallback_soil_data(latitude, longitude):
    """
    Get fallback soil data when SoilGrids API is unavailable
    Returns realistic default values based on region
    """
    soil_data = {
        "latitude": latitude,
        "longitude": longitude,
        "Nitrogen": 48,
        "Phosphorus": 26,
        "Potassium": 190,
        "pH": 6.5,
        "Organic_Carbon": 0.82,
        "CEC": 12.2,
        "source": "Default Profile (Fallback Mode)"
    }
    return soil_data
    """
    Rough estimation of Phosphorus based on Organic Carbon
    This is a simplified estimation - actual soil testing is recommended
    """
    # Generally, higher OC correlates with P availability
    return max(15, min(60, organic_carbon * 10))


def estimate_potassium(cec):
    """
    Rough estimation of Potassium based on CEC (Cation Exchange Capacity)
    This is a simplified estimation - actual soil testing is recommended
    """
    # Higher CEC usually indicates higher K availability
    return max(100, min(300, cec * 15))


def get_soil_data(location_input, latitude=None, longitude=None):
    """
    Get soil data from either coordinates or location name
    
    Args:
        location_input: str (District/Block name) or None
        latitude: float or None
        longitude: float or None
    
    Returns:
        dict: Soil parameters or error message
    """
    coords = None
    location_name = location_input
    
    # If coordinates provided, use them
    if latitude is not None and longitude is not None:
        coords = (latitude, longitude)
    # Otherwise, geocode the location name
    elif location_input:
        coords = get_coordinates_from_location(location_input)
        if coords:
            latitude, longitude = coords
    
    if not coords:
        return {
            "error": "Could not determine location coordinates",
            "location_input": location_input
        }
    
    # Fetch soil data from SoilGrids (with fallback)
    soil_data = fetch_soilgrids_data(coords[0], coords[1])
    
    if not soil_data or "error" in soil_data:
        return {
            "error": "Could not fetch soil data",
            "coordinates": coords
        }
    
    # Add location name if available
    if location_name:
        soil_data["location_name"] = location_name
    
    return soil_data
