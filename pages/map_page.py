import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

from services.weather import get_weather
from services.aqi import get_live_aqi


from utils.aqi_utils import (
    get_aqi_label,
    get_aqi_color,
    get_health_advice
)



def map_page():

    st.title("🗺️ Live India AQI Map")
    st.caption(
        "Live AQI and pollutant data from OpenWeather — refreshed every 10 minutes."
    )

    df = pd.read_csv("data/cities.csv")

    m = folium.Map(
        location=[22.5, 79],
        zoom_start=5,
        tiles="CartoDB positron"
    )

    for _, row in df.iterrows():

        city = row["City"]
        lat = row["Latitude"]
        lon = row["Longitude"]

        weather = get_weather(city)
        air = get_live_aqi(lat, lon)

        if air:
            live_aqi = air["aqi"]
            aqi_label = get_aqi_label(live_aqi)
            color = get_aqi_color(live_aqi)
            advice = get_health_advice(live_aqi)

            pollution_text = f"""
            OpenWeather AQI: {live_aqi} ({aqi_label})<br>
            PM2.5: {air['pm2_5']} µg/m³<br>
            PM10: {air['pm10']} µg/m³<br>
            NO₂: {air['no2']} µg/m³<br>
            O₃: {air['o3']} µg/m³<br>
            CO: {air['co']} µg/m³<br>
            """
        else:
            live_aqi = 3
            color = "gray"
            advice = "AQI data unavailable."
            pollution_text = "AQI data unavailable.<br>"

        if weather:
            weather_text = f"""
            Temperature: {weather['temperature']} °C<br>
            Humidity: {weather['humidity']} %<br>
            Wind: {weather['wind']} m/s<br>
            Condition: {weather['description']}<br>
            """
        else:
            weather_text = "Weather data unavailable.<br>"

        popup = f"""
        <b>{city}</b><br><br>
        {pollution_text}
        {weather_text}
        <b>Advice:</b> {advice}
        """

        folium.CircleMarker(
            location=[lat, lon],
            radius=10,
            popup=popup,
            tooltip=f"{city} - AQI {live_aqi}",
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.8
        ).add_to(m)

    st_folium(m, width=1200, height=650)

    st.caption("AQI is live from OpenWeather Air Pollution API. Scale: 1 Good → 5 Very Poor.")