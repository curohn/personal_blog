import os
import time
import requests
from datetime import datetime
from zoneinfo import ZoneInfo

ATLANTA_TZ = ZoneInfo("America/New_York")

_cache = {"data": None, "expires_at": 0}

ATLANTA_LAT = 33.749
ATLANTA_LON = -84.388
CACHE_TTL = 1800  # 30 minutes


def _period_from_hours(hour, sunrise, sunset):
    if hour >= sunset + 2 or hour < sunrise - 1:
        return "night"
    if hour < sunrise + 1:
        return "dawn"
    if hour < 12:
        return "morning"
    if hour < 14:
        return "noon"
    if hour < sunset - 1:
        return "afternoon"
    return "dusk"


def _period_simple(hour):
    if hour >= 21 or hour < 5:
        return "night"
    if hour < 7:
        return "dawn"
    if hour < 12:
        return "morning"
    if hour < 14:
        return "noon"
    if hour < 18:
        return "afternoon"
    return "dusk"


def _condition(weather_id):
    if 200 <= weather_id < 300:
        return "storm"
    if 300 <= weather_id < 600:
        return "rain"
    if 600 <= weather_id < 700:
        return "snow"
    if 700 <= weather_id < 800:
        return "fog"
    if weather_id == 800:
        return "clear"
    return "clouds"


def get_theme_data():
    now = time.monotonic()
    if _cache["data"] and now < _cache["expires_at"]:
        return _cache["data"]

    hour = datetime.now(ATLANTA_TZ).hour
    api_key = os.getenv("OPEN_WEATHER_MAP_API_KEY")

    if not api_key:
        result = _fallback(hour)
        _cache.update({"data": result, "expires_at": now + CACHE_TTL})
        return result

    try:
        resp = requests.get(
            "https://api.openweathermap.org/data/2.5/weather",
            params={"lat": ATLANTA_LAT, "lon": ATLANTA_LON, "appid": api_key},
            timeout=5,
        )
        resp.raise_for_status()
        data = resp.json()

        sunrise = datetime.fromtimestamp(data["sys"]["sunrise"], tz=ATLANTA_TZ).hour
        sunset = datetime.fromtimestamp(data["sys"]["sunset"], tz=ATLANTA_TZ).hour
        time_period = _period_from_hours(hour, sunrise, sunset)
        weather_condition = _condition(data["weather"][0]["id"])
        temp_f = round((data["main"]["temp"] - 273.15) * 9 / 5 + 32)
        description = data["weather"][0]["description"].title()
    except Exception:
        result = _fallback(hour)
        _cache.update({"data": result, "expires_at": now + CACHE_TTL})
        return result

    result = {
        "time_period": time_period,
        "weather_condition": weather_condition,
        "is_dark": time_period in ("night", "dawn", "dusk"),
        "temp_f": temp_f,
        "description": description,
    }
    _cache.update({"data": result, "expires_at": now + CACHE_TTL})
    return result


def _fallback(hour=None):
    if hour is None:
        hour = datetime.now(ATLANTA_TZ).hour
    period = _period_simple(hour)
    return {
        "time_period": period,
        "weather_condition": "clear",
        "is_dark": period in ("night", "dawn", "dusk"),
        "temp_f": None,
        "description": None,
    }
