"""
Project configuration.

Edit this file to configure which locations to fetch weather for and where to save output.

Options:
- LOCATIONS: list of location names (strings). If non-empty, these locations are used.
- LOCATION_SUFFIX: appended to each location when querying (e.g. "Papua Barat, Indonesia" or "Indonesia").
- OUTPUT_CSV: output CSV filename.
- USE_AQI: whether to request air quality data (True/False).

By default LOCATIONS is empty, so the script will try to read locations from INPUT_EXCEL for backward compatibility.
"""

# Example: specify a few locations directly
LOCATIONS = [
    "Aimas",
    "Beraur",
    "Klamono",
    "Klaso",
    "Klawak",
    "Klayili",
    "Makbon",
    "Maudus",
    "Mayamuk",
    "Moraid",
    "Salawati",
    "Salawati Selatan",
    "Sayosa",
    "Seget",
    "Segun",
    "Sorong"
]

# Append this suffix to each location when querying the API (set to empty string to use the raw name)
LOCATION_SUFFIX = "Indonesia"

# Where to write output
OUTPUT_CSV = "output.csv"

# Whether to request air-quality data (may increase API usage)
USE_AQI = True
