import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from services.weather import get_weather

def get_aqi_color(aqi):
    if aqi <= 50:
        return "green"
    elif aqi <= 100:
        return "blue"
    elif aqi <= 150:
        return "orange"
    elif aqi <= 200:
        return "red"
    else:
        return "darkred"

def get_health_advice(aqi):
    if aqi <= 50:
        return "Good air quality. Outdoor activities are safe."
    elif aqi <= 100:
        return "Moderate air quality. Sensitive people should be cautious."
    elif aqi <= 150:
        return "Unhealthy for sensitive groups. Reduce long outdoor activity."
    elif aqi <= 200:
        return "Poor air quality. Wear a mask outdoors."
    else:
        return "Very poor air quality. Avoid outdoor exposure."

def map_page():
    st.title("🗺️ Interactive India AQI Map")

    df = pd.read_csv("data/cities.csv")

    m = folium.Map(
        location=[22.5, 79],
        zoom_start=5,
        tiles="CartoDB positron"
    )

    for _, row in df.iterrows():
        city = row["City"]
        aqi = int(row["AQI"])

        weather = get_weather(city)

        if weather:
            weather_text = f"""
            🌡 Temp: {weather['temperature']} °C<br>
            💧 Humidity: {weather['humidity']} %<br>
            🌬 Wind: {weather['wind']} m/s<br>
            ☁ Condition: {weather['description']}<br>
            """
        else:
            weather_text = "Weather data unavailable<br>"

        popup = f"""
        <b>{city}</b><br>
        AQI: {aqi}<br>
        {weather_text}
        <b>Advice:</b> {get_health_advice(aqi)}
        """

        folium.CircleMarker(
            location=[row["Latitude"], row["Longitude"]],
            radius=10,
            popup=popup,
            tooltip=city,
            color=get_aqi_color(aqi),
            fill=True,
            fill_color=get_aqi_color(aqi),
            fill_opacity=0.8
        ).add_to(m)

    st_folium(m, width=1200, height=650)

    st.caption("AQI values are sample values for now. Weather is live from OpenWeather.")