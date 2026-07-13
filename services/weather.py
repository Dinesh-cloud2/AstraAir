import os
import requests
from pathlib import Path

env_path = Path(__file__).parent.parent / ".env"
API_KEY = os.getenv("OPENWEATHER_API_KEY")

with open(env_path, "r") as f:
    API_KEY = f.read().split("=")[1].strip()

def get_weather(city):
    print("API KEY LENGTH:", len(API_KEY))

    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?q={city}&appid={API_KEY}&units=metric"
    )

    response = requests.get(url)

    print("Status Code:", response.status_code)
    print("Response:", response.text)

    if response.status_code != 200:
        return None

    data = response.json()

    return {
        "temperature": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "wind": data["wind"]["speed"],
        "description": data["weather"][0]["description"].title(),
        "icon": data["weather"][0]["icon"]
    }