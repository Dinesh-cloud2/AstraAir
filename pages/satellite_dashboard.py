from datetime import date

import folium
import streamlit as st
from streamlit_folium import st_folium

from satellite.no2 import get_no2_tile_url


def satellite_dashboard():

    st.title("🛰️ Satellite Intelligence Dashboard")

    st.write(
        "Explore Sentinel-5P satellite observations "
        "of atmospheric NO₂ pollution over India."
    )

    # Keep satellite results after Streamlit reruns
    if "no2_tile_url" not in st.session_state:
        st.session_state.no2_tile_url = None

    if "no2_image_count" not in st.session_state:
        st.session_state.no2_image_count = 0

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        start_date = st.date_input(
            "Start Date",
            value=date(2025, 7, 1),
            key="satellite_start_date"
        )

    with col2:
        end_date = st.date_input(
            "End Date",
            value=date(2025, 7, 10),
            key="satellite_end_date"
        )

    opacity = st.slider(
        "Satellite Layer Opacity",
        min_value=0.2,
        max_value=1.0,
        value=0.7,
        step=0.1,
        key="satellite_opacity"
    )

    if start_date >= end_date:
        st.error("End Date must be later than Start Date.")
        return

    col_load, col_clear = st.columns([1, 1])

    with col_load:
        load_clicked = st.button(
            "🛰️ Load Satellite Data",
            type="primary",
            use_container_width=True
        )

    with col_clear:
        clear_clicked = st.button(
            "Clear Map",
            use_container_width=True
        )

    if clear_clicked:
        st.session_state.no2_tile_url = None
        st.session_state.no2_image_count = 0
        st.rerun()

    if load_clicked:
        with st.spinner(
            "Processing Sentinel-5P NO₂ observations..."
        ):
            tile_url, image_count = get_no2_tile_url(
                start_date.strftime("%Y-%m-%d"),
                end_date.strftime("%Y-%m-%d")
            )

        st.session_state.no2_tile_url = tile_url
        st.session_state.no2_image_count = image_count

    tile_url = st.session_state.no2_tile_url
    image_count = st.session_state.no2_image_count

    if tile_url:

        st.success(
            f"Loaded {image_count} Sentinel-5P observations."
        )

        satellite_map = folium.Map(
            location=[22.5, 79.0],
            zoom_start=5,
            tiles="CartoDB positron"
        )

        folium.TileLayer(
            tiles=tile_url,
            attr="Google Earth Engine / Sentinel-5P",
            name="Sentinel-5P NO₂",
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
            key="persistent_no2_map"
        )

        st.caption(
            "🔵 Lower NO₂ → 🟢 Moderate → 🟡 Elevated → 🔴 Higher NO₂"
        )

        st.divider()

        st.subheader("🧠 Satellite Interpretation")

        st.info(
            """
Higher satellite-observed NO₂ may be influenced by:

- Urban traffic emissions
- Industrial combustion
- Thermal power generation
- Biomass burning

Satellite observations provide coverage in areas where ground
monitoring stations may be limited.
"""
        )

    else:
        st.info(
            "Choose a valid date range and click "
            "**Load Satellite Data**."
        )