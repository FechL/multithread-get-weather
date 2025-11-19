# Multithreaded Weather Fetcher

This program retrieves current weather (and optionally air quality) for multiple locations using multithreading and the WeatherAPI service. Results are written to a CSV file.

![WeatherAPI Logo](img/logo.png)

[WeatherAPI](https://www.weatherapi.com) is a real-time weather data platform that provides current conditions, forecasts, air quality, astronomy, and historical weather information through API endpoints.

## Setup

1. Install dependencies from `requirements.txt`:

```bash
pip install -r requirements.txt
```

2. Create a `.env` file in the project root containing your API key:

```bash
API_KEY=<your_weatherapi_key>
```

3. Configure which locations to fetch in `configuration.py`.

- You MUST set `LOCATIONS` to a non-empty list of location names in `configuration.py`.
- Optionally set `LOCATION_SUFFIX` (e.g. `"Papua Barat, Indonesia"`) to append to queries.
- Use `OUTPUT_CSV` to change the output filename (default: `output.csv`).
- Set `USE_AQI = True` to request air quality (may use additional API quota).

## Run

From the project root run:

```bash
python get_weather.py
```

## Output

By default, results are saved to `output.csv` (or the filename configured in `configuration.py`).

## Notes

- The project no longer reads locations from an Excel file. Provide locations via `configuration.py`.
- The script uses `API_KEY` from `.env` (requires `python-dotenv`).