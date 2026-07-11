from datetime import date

import folium
import streamlit as st
from streamlit_folium import st_folium

from satellite.no2 import get_no2_tile_url
from satellite.hcho import get_hcho_tile_url


def satellite_dashboard():

    st.title("🛰️ Satellite Intelligence Dashboard")

    if "satellite_tile_url" not in st.session_state:
        st.session_state.satellite_tile_url = None

    if "satellite_image_count" not in st.session_state:
        st.session_state.satellite_image_count = 0

    if "satellite_layer_name" not in st.session_state:
        st.session_state.satellite_layer_name = ""

    dataset = st.selectbox(
        "Select Satellite Dataset",
        [
            "Sentinel-5P NO₂",
            "Sentinel-5P HCHO (Formaldehyde)"
        ]
    )

    col1, col2 = st.columns(2)

    with col1:
        start_date = st.date_input(
            "Start Date",
            value=date(2025, 7, 1),
            key="satellite_start"
        )

    with col2:
        end_date = st.date_input(
            "End Date",
            value=date(2025, 7, 10),
            key="satellite_end"
        )

    opacity = st.slider(
        "Layer Opacity",
        0.2,
        1.0,
        0.7,
        0.1
    )

    if start_date >= end_date:
        st.error("End Date must be later than Start Date.")
        return

    load_col, clear_col = st.columns(2)

    with load_col:
        load_clicked = st.button(
            "🛰️ Load Satellite Data",
            type="primary",
            use_container_width=True
        )

    with clear_col:
        clear_clicked = st.button(
            "Clear Map",
            use_container_width=True
        )

    if clear_clicked:
        st.session_state.satellite_tile_url = None
        st.session_state.satellite_image_count = 0
        st.session_state.satellite_layer_name = ""
        st.rerun()

    if load_clicked:
        with st.spinner("Processing satellite observations..."):

            start = start_date.strftime("%Y-%m-%d")
            end = end_date.strftime("%Y-%m-%d")

            if dataset == "Sentinel-5P NO₂":
                tile_url, image_count = get_no2_tile_url(start, end)
                layer_name = "Sentinel-5P NO₂"

            else:
                tile_url, image_count = get_hcho_tile_url(start, end)
                layer_name = "Sentinel-5P HCHO"

        st.session_state.satellite_tile_url = tile_url
        st.session_state.satellite_image_count = image_count
        st.session_state.satellite_layer_name = layer_name

    tile_url = st.session_state.satellite_tile_url
    image_count = st.session_state.satellite_image_count
    layer_name = st.session_state.satellite_layer_name

    if tile_url:

        st.success(
            f"Loaded {image_count} observations for {layer_name}."
        )

        satellite_map = folium.Map(
            location=[22.5, 79.0],
            zoom_start=5,
            tiles="CartoDB positron"
        )

        folium.TileLayer(
            tiles=tile_url,
            attr="Google Earth Engine / Sentinel-5P",
            name=layer_name,
            overlay=True,
            control=True,
            opacity=opacity
        ).add_to(satellite_map)

        folium.LayerControl(
            collapsed=False
        ).add_to(satellite_map)

        st_folium(
            satellite_map,
            width=None,
            height=650,
            key="persistent_satellite_map"
        )

        st.divider()

        if layer_name == "Sentinel-5P NO₂":
            st.subheader("🧠 NO₂ Interpretation")
            st.info(
                """
Higher NO₂ may be associated with:

- Road traffic emissions
- Industrial combustion
- Thermal power plants
- Biomass burning
"""
            )

        else:
            st.subheader("🧪 HCHO / Formaldehyde Interpretation")
            st.info(
                """
Higher HCHO may be associated with:

- Biomass and crop-residue burning
- Volatile organic compound emissions
- Industrial chemical activity
- Wildfire and vegetation-related emissions
"""
            )

    else:
        st.info("Select a dataset and click **Load Satellite Data**.")