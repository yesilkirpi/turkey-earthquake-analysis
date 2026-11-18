import requests
import pandas as pd
from datetime import date

URL = "https://earthquake.usgs.gov/fdsnws/event/1/query"

def fetch_data():
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
    return response.json()

#turn data into table
def to_dataframe(data):
    rows = []
    for feature in data["features"]:
        props = feature["properties"]
        coords = feature["geometry"]["coordinates"]
        rows.append({
            "time": pd.to_datetime(props["time"], unit="ms"),
            "magnitude": props["mag"],
            "place": props["place"],
            "longtitude": coords[0],
            "latitude": coords[1],
            "depth": coords[2],
        })
    return pd.DataFrame(rows)

if __name__ == "__main__":
    data = fetch_data()
    df = to_dataframe(data)
    print(df.head())
    print(df.shape)
    df.to_csv("data/earthquakes.csv", index=False)