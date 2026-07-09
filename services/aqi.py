import requests
from pathlib import Path


env_path = Path(__file__).parent.parent / ".env"

with open(env_path, "r") as f:
    API_KEY = f.read().split("=")[1].strip()


def get_live_aqi(lat, lon):
    url = (
        "https://api.openweathermap.org/data/2.5/air_pollution"
        f"?lat={lat}&lon={lon}&appid={API_KEY}"
    )

    response = requests.get(url)

    if response.status_code != 200:
        return None

    data = response.json()
    item = data["list"][0]

    return {
        "aqi": item["main"]["aqi"],
        "co": item["components"]["co"],
        "no2": item["components"]["no2"],
        "o3": item["components"]["o3"],
        "pm2_5": item["components"]["pm2_5"],
        "pm10": item["components"]["pm10"]
    }