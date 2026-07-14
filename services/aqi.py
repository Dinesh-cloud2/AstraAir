import os
from pathlib import Path

import requests
import streamlit as st
from dotenv import load_dotenv


env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path, override=True)

API_KEY = os.getenv("OPENWEATHER_API_KEY")


@st.cache_data(ttl=600, show_spinner=False)
def get_live_aqi(lat, lon):

    url = (
        "https://api.openweathermap.org/data/2.5/air_pollution"
        f"?lat={lat}&lon={lon}&appid={API_KEY}"
    )

    try:
        response = requests.get(url, timeout=10)

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
            "pm10": item["components"]["pm10"],
        }

    except requests.RequestException:
        return None