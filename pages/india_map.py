import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

st.title("🌍 India AQI Map")

df = pd.read_csv("data/cities.csv")

m = folium.Map(
    location=[22.5, 79],
    zoom_start=5,
    tiles="CartoDB Positron"
)

for _, row in df.iterrows():

    color = "green"

    if row["AQI"] > 150:
        color = "red"
    elif row["AQI"] > 100:
        color = "orange"

    folium.CircleMarker(
        location=[row["Latitude"], row["Longitude"]],
        radius=10,
        color=color,
        fill=True,
        fill_opacity=0.8,
        popup=f"""
        <b>{row['City']}</b><br>
        AQI : {row['AQI']}
        """
    ).add_to(m)

st_folium(m, width=1200, height=650)