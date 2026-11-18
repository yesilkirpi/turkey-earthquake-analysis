import requests
from datetime import date

URL = "https://earthquake.usgs.gov/fdsnws/event/1/query"

params = {
    "format": "geojson",
    "starttime": "2025-01-01",
    "endtime": date.today().isoformat(),
    "minmagnitude": 3,
    "minlatitude": 35.5,
    "maxlatitude": 42.5,
    "minlongitude": 25.5,
    "maxlongitude": 45,
}

response = requests.get(URL, params=params, timeout=30)
response.raise_for_status()
data = response.json()

print(len(data["features"]))