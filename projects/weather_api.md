# Weather API

This site themes itself based on Atlanta's real-time weather and time of day. Here's how that works under the hood.

## The API

The site uses the [OpenWeatherMap](https://openweathermap.org/) Current Weather endpoint:

```
GET https://api.openweathermap.org/data/2.5/weather
    ?lat=33.749&lon=-84.388&appid={API_KEY}
```

Atlanta's coordinates are hardcoded. The response is a JSON object that includes the current temperature, a weather condition ID, and Unix timestamps for today's sunrise and sunset.

## Time of Day

The response includes `sys.sunrise` and `sys.sunset` as Unix timestamps. These get converted to local hours and used to divide the day into six periods:

| Period | Condition |
|---|---|
| `night` | After sunset+2h or before sunrise-1h |
| `dawn` | Within 1 hour of sunrise |
| `morning` | Sunrise+1h through noon |
| `noon` | 12pm – 2pm |
| `afternoon` | 2pm through sunset-1h |
| `dusk` | Last hour before sunset+2h |

Using actual sunrise/sunset data means the transitions shift with the seasons — dawn in December starts later than in June.

## Weather Condition

OWM uses a numeric ID system for weather conditions. The site maps ranges of those IDs to six buckets:

| ID Range | Condition |
|---|---|
| 200–299 | `storm` |
| 300–599 | `rain` |
| 600–699 | `snow` |
| 700–799 | `fog` |
| 800 | `clear` |
| 801–899 | `clouds` |

## Caching

The API is only called once every 30 minutes. The result is stored in a simple in-memory dict with a `time.monotonic()` expiry:

```python
_cache = {"data": None, "expires_at": 0}
CACHE_TTL = 1800  # seconds

def get_theme_data():
    now = time.monotonic()
    if _cache["data"] and now < _cache["expires_at"]:
        return _cache["data"]
    # ... fetch and store
    _cache.update({"data": result, "expires_at": now + CACHE_TTL})
```

This avoids hitting the API on every page load. The tradeoff is that the theme can lag up to 30 minutes behind actual conditions.

## Fallback

If the API key is missing or the request fails, the site falls back to a time-only estimate using fixed hour boundaries (no sunrise/sunset data), and defaults to `clear` for the weather condition. The site still themes correctly, just without live weather data.

## Injecting into Templates

Flask's `@app.context_processor` makes the result available in every template automatically — no per-route changes needed:

```python
@app.context_processor
def inject_theme():
    data = get_theme_data()
    return {"theme_data": data}
```

The body class is then set in `base.html`:

```html
<body class="time-{{ theme_data.time_period }} weather-{{ theme_data.weather_condition }}">
```

All CSS theme variables and canvas effects key off those two body classes.
