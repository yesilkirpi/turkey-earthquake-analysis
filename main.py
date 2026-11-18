import requests
import pandas as pd
import matplotlib.pyplot as plt
import folium
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
            "longitude": coords[0],
            "latitude": coords[1],
            "depth": coords[2],
        })
    return pd.DataFrame(rows)

#graph functions

def plot_monthly_counts(df):
    counts = df["time"].dt.to_period("M").value_counts().sort_index()
    counts.plot(kind="bar", figsize=(10, 5))
    plt.title("Monthly earthquake count(M3+)")
    plt.xlabel("Month")
    plt.ylabel("Number of earthquakes")
    plt.tight_layout()
    plt.savefig("outputs/monthly_counts.png", dpi=150)
    plt.close()

def plot_magnitude_histogram(df):
    plt.figure(figsize=(8, 5))
    plt.hist(df["magnitude"], bins=20, edgecolor="blue")
    plt.title("Magnitude distribution")
    plt.xlabel("Magnitude")
    plt.tight_layout()
    plt.savefig("outputs/magnitude_histogram.png", dpi=150)
    plt.close()

def plot_map(df):
    plt.figure(figsize=(10, 6))
    sc = plt.scatter(df["longitude"], df["latitude"],
                     c=df["magnitude"], s=df["magnitude"] ** 3,
                     cmap="Reds", alpha=0.6, edgecolor="black", linewidth=0.3)
    plt.colorbar(sc, label="Magnitude")
    plt.title("Earthquake locations")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.tight_layout()
    plt.savefig("outputs/map.png", dpi=150)
    plt.close()

def plot_interantive_map(df):
    m = folium.Map(location=[39, 35], zoom_start=6)
    for _, row in df.iterrows():
        if row["magnitude"] >= 5:
            color = "red"
        elif row["magnitude"] >= 4:
            color = "orange"
        else:
            color = "blue"

        folium.CircleMarker(
            location=[row["latitude"], row["longitude"]],

            radius = row["magnitude"] * 1.5,
            color = color,
            fill = True,
            fill_opacity = 0.5,

            popup=f"M{row['magnitude']} | {row['place']} | {row['time']:%Y-%m-%d} | depth {row['depth']} km",

        ).add_to(m)

        m.save("outputs/map.html")


if __name__ == "__main__":
    data = fetch_data()
    df = to_dataframe(data)
    before = len(df)
    df = df[df["place"].str.contains("Turkey|Türkiye", na = False)]
    print(f"Kept {len(df)} of {before} rows")
    print(df.head())
    print(df.shape)
    df.to_csv("data/earthquakes.csv", index=False)
    plot_monthly_counts(df)
    plot_magnitude_histogram(df)
    plot_map(df)