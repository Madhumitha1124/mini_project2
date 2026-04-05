import requests
from django.conf import settings


MARKET_CROP_ALIASES = {
    "Kidney Beans": "Pulses",
    "Pigeon Peas": "Pulses",
    "Moth Beans": "Pulses",
    "Mung Bean": "Pulses",
    "Black Gram": "Pulses",
    "Lentil": "Pulses",
    "Chickpea": "Pulses",
    "Muskmelon": "Vegetables",
    "Watermelon": "Vegetables",
    "Papaya": "Banana",
}

MARKET_QUERY_FALLBACKS = {
    "Sorghum": ["Jowar"],
    "Pigeon Peas": ["Arhar (Tur/Red Gram)(Whole)", "Arhar"],
    "Black Gram": ["Urad", "Black Gram (Urd Beans)(Whole)"],
    "Mung Bean": ["Moong", "Green Gram (Moong)(Whole)"],
    "Chickpea": ["Gram", "Bengal Gram (Gram)(Whole)"],
    "Cotton": ["Kapas"],
}

OFFLINE_DEFAULT_MARKET_PRICES = {
    "Rice": 3200.0,
    "Maize": 2400.0,
    "Chickpea": 5600.0,
    "Kidney Beans": 6800.0,
    "Pigeon Peas": 7000.0,
    "Moth Beans": 6200.0,
    "Mung Bean": 7200.0,
    "Black Gram": 7100.0,
    "Lentil": 6400.0,
    "Pomegranate": 5200.0,
    "Banana": 2000.0,
    "Mango": 3800.0,
    "Grapes": 5200.0,
    "Watermelon": 1800.0,
    "Muskmelon": 2200.0,
    "Apple": 8000.0,
    "Orange": 4200.0,
    "Papaya": 2600.0,
    "Coconut": 3000.0,
    "Cotton": 7600.0,
    "Sugarcane": 340.0,
    "Tobacco": 9000.0,
    "Pulses": 6500.0,
    "Vegetables": 2500.0,
    "Sorghum": 2900.0,
}


def get_weather_for_city(city: str):
    """Return dict with keys: temp (C), humidity (%), rain (mm) or None on failure."""
    key = getattr(settings, "WEATHER_API_KEY", None)
    if not key or not city:
        return None

    try:
        url = "https://api.openweathermap.org/data/2.5/weather"
        params = {"q": city, "appid": key, "units": "metric"}
        resp = requests.get(url, params=params, timeout=6)
        resp.raise_for_status()
        j = resp.json()

        temp = j.get("main", {}).get("temp")
        humidity = j.get("main", {}).get("humidity")
        # rainfall may be under 'rain' (1h or 3h)
        rain = 0
        if "rain" in j:
            rain = j.get("rain", {}).get("1h", j.get("rain", {}).get("3h", 0))

        return {"temp": temp, "humidity": humidity, "rain": rain}
    except Exception:
        return None


def _to_float(value, default=0.0):
    try:
        if value is None:
            return float(default)
        cleaned = str(value).replace(",", "").strip()
        return float(cleaned)
    except Exception:
        return float(default)


def _normalize_crop_for_market(crop_name: str):
    if not crop_name:
        return ""
    crop_title = crop_name.strip().title()
    return MARKET_CROP_ALIASES.get(crop_title, crop_title)


def _offline_market_payload(crop_name: str, reason: str):
    normalized = _normalize_crop_for_market(crop_name)
    base_crop = (crop_name or "").strip().title()
    modal_price = OFFLINE_DEFAULT_MARKET_PRICES.get(base_crop)
    if modal_price is None:
        modal_price = OFFLINE_DEFAULT_MARKET_PRICES.get(normalized, 2800.0)

    min_price = round(modal_price * 0.92, 2)
    max_price = round(modal_price * 1.08, 2)

    return {
        "crop": normalized or crop_name,
        "market": "Offline Estimate",
        "district": "-",
        "state": "-",
        "min_price": min_price,
        "max_price": max_price,
        "modal_price": round(modal_price, 2),
        "unit": "₹ / Quintal",
        "date": "Not available",
        "source": f"Offline default ({reason})",
        "live": False,
    }


def get_market_data_for_crop(crop_name: str):
    """
    Return crop-wise market data.
    - Uses only data.gov.in Agmarknet API.
    - Does not use built-in indicative fallback prices.
    """
    normalized_crop = _normalize_crop_for_market(crop_name)
    market_key = getattr(settings, "MARKET_DATA_API_KEY", "").strip()
    resource_id = getattr(settings, "MARKET_DATA_RESOURCE_ID", "9ef84268-d588-465a-a308-a864a43d0070").strip()

    if not market_key:
        return _offline_market_payload(crop_name, "API key not configured")

    if not normalized_crop or not resource_id:
        return _offline_market_payload(crop_name, "invalid live API request")

    last_error = ""
    try:
        url = f"https://api.data.gov.in/resource/{resource_id}"
        query_candidates = [normalized_crop]
        query_candidates.extend(MARKET_QUERY_FALLBACKS.get(normalized_crop, []))

        seen = set()
        query_candidates = [
            candidate
            for candidate in query_candidates
            if candidate and not (candidate in seen or seen.add(candidate))
        ]

        for commodity in query_candidates:
            params = {
                "api-key": market_key,
                "format": "json",
                "limit": 1,
                "filters[commodity]": commodity,
            }
            for timeout_seconds in (8, 15, 25):
                try:
                    resp = requests.get(url, params=params, timeout=timeout_seconds)
                    resp.raise_for_status()
                    payload = resp.json() or {}
                    records = payload.get("records", [])
                    if records:
                        best = records[0]
                        min_price = _to_float(best.get("min_price"), 0.0)
                        max_price = _to_float(best.get("max_price"), 0.0)
                        modal_price = _to_float(best.get("modal_price"), 0.0)
                        return {
                            "crop": normalized_crop,
                            "market": best.get("market") or "Unknown Market",
                            "district": best.get("district") or "-",
                            "state": best.get("state") or "-",
                            "min_price": round(min_price, 2),
                            "max_price": round(max_price, 2),
                            "modal_price": round(modal_price, 2),
                            "unit": "₹ / Quintal",
                            "date": best.get("arrival_date") or best.get("timestamp") or "-",
                            "source": f"data.gov.in (Agmarknet: {commodity})",
                            "live": True,
                        }
                except requests.RequestException as request_error:
                    status_code = getattr(getattr(request_error, "response", None), "status_code", None)
                    if status_code:
                        last_error = f"HTTP {status_code}"
                    else:
                        last_error = request_error.__class__.__name__
                    continue
    except Exception:
        pass

    reason = f"live data unavailable from data.gov.in{(': ' + last_error[:120]) if last_error else ''}"
    return _offline_market_payload(crop_name, reason)
