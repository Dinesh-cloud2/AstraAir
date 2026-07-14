import os
from pathlib import Path

import requests
import streamlit as st
from dotenv import load_dotenv


env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path, override=True)

API_KEY = os.getenv("OPENWEATHER_API_KEY")

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


@st.cache_data(ttl=600, show_spinner=False)
def get_weather(city=None, lat=None, lon=None):

    if not API_KEY:
        return None

    params = {
        "appid": API_KEY,
        "units": "metric",
    }

    # Coordinates are more reliable
    if lat is not None and lon is not None:
        params["lat"] = lat
        params["lon"] = lon

    elif city:
        params["q"] = city

    else:
        return None

    try:
        response = requests.get(
            BASE_URL,
            params=params,
            timeout=10,
        )

        if response.status_code != 200:
            return None

        data = response.json()

        return {
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "wind": data["wind"]["speed"],
            "description": (
                data["weather"][0]["description"].title()
            ),
            "icon": data["weather"][0]["icon"],
        }

    except requests.RequestException:
        return None