from datetime import date, timedelta

import folium
import streamlit as st
from streamlit_folium import st_folium

from satellite.no2 import get_no2_tile_url


def satellite_page():
    st.title("🛰️ Sentinel-5P NO₂ Explorer")
    st.caption(
        "Satellite layers use the selected historical date range. "
        "Live AQI and weather are current observations."
   )

    st.info(
    """
    ### Satellite Layer

    This page visualizes **Sentinel-5P satellite observations**
    processed through **Google Earth Engine**.

    Current layer:
    - 🟠 Tropospheric NO₂
    - Historical satellite imagery
    - India coverage

    Choose a date range below to visualize pollution patterns.
    """
    )
        

    today = date.today()
    default_start = today - timedelta(days=7)

    col1, col2 = st.columns(2)

    with col1:
        start_date = st.date_input(
            "Start date",
            value=default_start,
            max_value=today,
        )

    with col2:
        end_date = st.date_input(
            "End date",
            value=today,
            max_value=today,
        )

    opacity = st.slider(
        "Satellite layer opacity",
        min_value=0.1,
        max_value=1.0,
        value=0.75,
        step=0.05,
    )

    if start_date >= end_date:
        st.error("End date must be later than start date.")
        return

    with st.spinner("Loading Sentinel-5P NO₂ data..."):
        tile_url, image_count = get_no2_tile_url(
            start_date.strftime("%Y-%m-%d"),
            end_date.strftime("%Y-%m-%d"),
            opacity,
        )

    if not tile_url:
        st.warning("No Sentinel-5P NO₂ images found for this date range.")
        return

    st.success(
        f"Successfully loaded **{image_count} Sentinel-5P observations**."
    )

    satellite_map = folium.Map(
        location=[22.5, 79.0],
        zoom_start=5,
        tiles="CartoDB positron",
    )

    folium.TileLayer(
        tiles=tile_url,
        attr="Google Earth Engine / Sentinel-5P",
        name="Sentinel-5P NO₂",
        overlay=True,
        control=True,
        opacity=opacity,
    ).add_to(satellite_map)

    folium.LayerControl().add_to(satellite_map)

    st_folium(
        satellite_map,
        width=1200,
        height=650,
    )

    st.caption(
        """
        Blue → Lower NO₂ concentration

        Yellow / Orange → Moderate concentration

        Red → Higher NO₂ concentration
        
        Sentinel-5P • Google Earth Engine
        """
    )