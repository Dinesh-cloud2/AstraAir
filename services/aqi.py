from pathlib import Path

import requests
import streamlit as st
from dotenv import load_dotenv


env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)


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
def get_live_aqi(lat, lon):

    api_key = get_api_key()

    if not api_key:
        st.error(
            "OPENWEATHER_API_KEY is missing in Streamlit Secrets."
        )
        return None

    url = (
        "https://api.openweathermap.org/data/2.5/air_pollution"
    )

    params = {
        "lat": lat,
        "lon": lon,
        "appid": api_key,
    }

    try:
        response = requests.get(
            url,
            params=params,
            timeout=10,
        )

        if response.status_code != 200:
            st.error(
                f"OpenWeather AQI API error: "
                f"{response.status_code}"
            )
            st.code(response.text)
            return None

        data = response.json()

        if not data.get("list"):
            st.error("OpenWeather returned no AQI observations.")
            return None

        item = data["list"][0]
        components = item["components"]

        return {
            "aqi": item["main"]["aqi"],
            "co": components.get("co"),
            "no2": components.get("no2"),
            "o3": components.get("o3"),
            "pm2_5": components.get("pm2_5"),
            "pm10": components.get("pm10"),
        }

    except requests.RequestException as error:
        st.error(f"AQI request failed: {error}")
        return None