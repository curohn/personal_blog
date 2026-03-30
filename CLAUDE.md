# Personal Blog — Claude Context

## Overview
Portfolio/blog site for John Curran. Flask backend, plain HTML/CSS/JS frontend. Deployed on Render at j-curran.com.

## Running Locally
```
python -m flask run --debug
```
Requires `.env` with `OPEN_WEATHER_MAP_API_KEY` and `SECRET_KEY`.

## Stack
- **Backend**: Flask 3.1, Python 3.13
- **Frontend**: HTML, CSS custom properties, vanilla JS (no frameworks)
- **Content**: Markdown files in `/projects/` rendered at runtime
- **Deployment**: Render (Gunicorn)

## Key Architecture

### Weather Theming (`weather.py`)
Fetches Atlanta weather from OpenWeatherMap every 30 min (in-memory cache). Returns:
- `time_period`: `night | dawn | morning | noon | afternoon | dusk` (derived from actual sunrise/sunset)
- `weather_condition`: `clear | clouds | rain | storm | snow | fog`
- `is_dark`: bool for favicon/icon switching

Injected into every template via `@app.context_processor`. Applied as body classes `time-X weather-Y`. All theme colors are CSS custom properties defined per class in `style.css`.

**Debug preview**: run with `--debug` and append `?time=dawn&weather=storm` to any URL.

### Routes
| URL | Function | Template |
|---|---|---|
| `/` | `home` | `home.html` |
| `/projects` | `research_and_projects` | `research_and_projects.html` |
| `/projects/<name>` | `project_detail` | `project_detail.html` (markdown) |
| `/projects/murmuration` | `murmuration` | `murmuration.html` (canvas sim) |
| `/about` | `experience_and_education` | `experience_and_education.html` |
| `/download_resume` | `download_resume` | — |

### Visual Effects (JS)
- `static/js/sun-effect.js` — radial glow orb, position by time of day, opacity scaled by weather. `z-index: 400`.
- `static/js/weather-effects.js` — rain/storm drops + wind streaks + lightning flashes + fog blobs + snow flakes. `z-index: 500`.
- `static/js/murmuration.js` — boid flocking simulation (separation, alignment, cohesion) with live controls.

### Adding a New Project
1. Add entry to `projects` list in `app.py`
2. Create `projects/<name>.md` for markdown content
3. If it needs a custom page (like murmuration), add a dedicated route and template

## CSS Theme Variables
All colors use `--bg-color`, `--card-bg`, `--text-color`, `--text-secondary`, `--alt-color`, `--border-color`, `--highlight-color`, `--shadow-color`, `--button-bg/text`, `--header-color/text`, `--footer-color/text`. Never hardcode colors — always use these variables.
