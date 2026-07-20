from pathlib import Path

import requests
import streamlit as st
from dotenv import load_dotenv


env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

BASE_URL = (
    "https://api.openweathermap.org/data/2.5/weather"
)


def get_api_key():
    try:
        key = st.secrets.get("OPENWEATHER_API_KEY")
        if key:
            return str(key)
    except Exception:
        pass

    import os

    return os.getenv("OPENWEATHER_API_KEY")


@st.cache_data(ttl=600, show_spinner=False)
def get_weather(city=None, lat=None, lon=None):

    api_key = get_api_key()

    if not api_key:
        st.error(
            "OPENWEATHER_API_KEY is missing in Streamlit Secrets."
        )
        return None

    params = {
        "appid": api_key,
        "units": "metric",
    }

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
            st.error(
                f"OpenWeather Weather API error: "
                f"{response.status_code}"
            )
            st.code(response.text)
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

    except requests.RequestException as error:
        st.error(f"Weather request failed: {error}")
        return None