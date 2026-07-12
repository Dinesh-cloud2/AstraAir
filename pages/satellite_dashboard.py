from datetime import date

import folium
import streamlit as st
from streamlit_folium import st_folium

from satellite.aerosol import get_aerosol_tile_url
from satellite.fires import get_fire_tile_url
from satellite.hcho import get_hcho_tile_url
from satellite.no2 import get_no2_tile_url

from services.satellite_intelligence import (
    generate_satellite_interpretation,
    get_region_names,
    get_satellite_evidence,
)


def satellite_dashboard():
    st.title("🛰️ Satellite Intelligence Dashboard")

    # ---------- Session state ----------

    if "satellite_tile_url" not in st.session_state:
        st.session_state.satellite_tile_url = None

    if "satellite_image_count" not in st.session_state:
        st.session_state.satellite_image_count = 0

    if "satellite_layer_name" not in st.session_state:
        st.session_state.satellite_layer_name = ""

    if "satellite_evidence" not in st.session_state:
        st.session_state.satellite_evidence = None

    if "satellite_analysis" not in st.session_state:
        st.session_state.satellite_analysis = None

    # ---------- Dataset selector ----------

    dataset = st.selectbox(
        "Select Satellite Dataset",
        [
            "Sentinel-5P NO₂",
            "Sentinel-5P HCHO (Formaldehyde)",
            "Sentinel-5P Aerosol Index",
            "NASA FIRMS Fire Hotspots",
        ],
    )

    # ---------- Regional evidence selector ----------

    region_name = st.selectbox(
        "Select Evidence Analysis Region",
        get_region_names(),
    )

    # ---------- Date selection ----------

    col1, col2 = st.columns(2)

    with col1:
        start_date = st.date_input(
            "Start Date",
            value=date(2025, 7, 1),
            key="satellite_start",
        )

    with col2:
        end_date = st.date_input(
            "End Date",
            value=date(2025, 7, 10),
            key="satellite_end",
        )

    opacity = st.slider(
        "Layer Opacity",
        min_value=0.2,
        max_value=1.0,
        value=0.7,
        step=0.1,
    )

    if start_date >= end_date:
        st.error("End Date must be later than Start Date.")
        return

    # ---------- Buttons ----------

    load_col, clear_col = st.columns(2)

    with load_col:
        load_clicked = st.button(
            "🛰️ Load Satellite Data",
            type="primary",
            use_container_width=True,
        )

    with clear_col:
        clear_clicked = st.button(
            "Clear Map",
            use_container_width=True,
        )

    if clear_clicked:
        st.session_state.satellite_tile_url = None
        st.session_state.satellite_image_count = 0
        st.session_state.satellite_layer_name = ""
        st.session_state.satellite_evidence = None
        st.session_state.satellite_analysis = None

        st.rerun()

    # ---------- Load selected map layer ----------

    if load_clicked:
        with st.spinner(
            "Processing satellite observations..."
        ):
            start = start_date.strftime("%Y-%m-%d")
            end = end_date.strftime("%Y-%m-%d")

            if dataset == "Sentinel-5P NO₂":
                tile_url, image_count = (
                    get_no2_tile_url(start, end)
                )

                layer_name = "Sentinel-5P NO₂"

            elif dataset == (
                "Sentinel-5P HCHO (Formaldehyde)"
            ):
                tile_url, image_count = (
                    get_hcho_tile_url(start, end)
                )

                layer_name = "Sentinel-5P HCHO"

            elif dataset == (
                "Sentinel-5P Aerosol Index"
            ):
                tile_url, image_count = (
                    get_aerosol_tile_url(start, end)
                )

                layer_name = (
                    "Sentinel-5P Aerosol Index"
                )

            else:
                tile_url, image_count = (
                    get_fire_tile_url(start, end)
                )

                layer_name = (
                    "NASA FIRMS Fire Hotspots"
                )

        st.session_state.satellite_tile_url = tile_url
        st.session_state.satellite_image_count = (
            image_count
        )
        st.session_state.satellite_layer_name = (
            layer_name
        )

        # Clear old evidence when new dates/data are loaded
        st.session_state.satellite_evidence = None
        st.session_state.satellite_analysis = None

    tile_url = st.session_state.satellite_tile_url
    image_count = (
        st.session_state.satellite_image_count
    )
    layer_name = (
        st.session_state.satellite_layer_name
    )

    # ---------- Display map ----------

    if tile_url:
        st.success(
            f"Loaded {image_count} observations "
            f"for {layer_name}."
        )

        satellite_map = folium.Map(
            location=[22.5, 79.0],
            zoom_start=5,
            tiles="CartoDB positron",
        )

        folium.TileLayer(
            tiles=tile_url,
            attr=(
                "Google Earth Engine / "
                "Satellite Data"
            ),
            name=layer_name,
            overlay=True,
            control=True,
            opacity=opacity,
        ).add_to(satellite_map)

        folium.LayerControl(
            collapsed=False
        ).add_to(satellite_map)

        st_folium(
            satellite_map,
            width=None,
            height=650,
            key="persistent_satellite_map",
        )

        st.divider()

        # ---------- Regional Evidence Engine ----------

        st.subheader(
            "🧠 Regional Satellite Evidence Engine"
        )

        st.write(
            f"Selected region: **{region_name}**"
        )

        analyze_clicked = st.button(
            "🔬 Analyze Regional Satellite Evidence",
            use_container_width=True,
        )

        if analyze_clicked:
            with st.spinner(
                f"Analyzing satellite evidence "
                f"for {region_name}..."
            ):
                evidence = get_satellite_evidence(
                    start_date.strftime("%Y-%m-%d"),
                    end_date.strftime("%Y-%m-%d"),
                    region_name,
                )

            if evidence is None:
                st.session_state.satellite_evidence = None
                st.session_state.satellite_analysis = None

                st.warning(
                    "Insufficient satellite observations "
                    "for the selected region and date range."
                )

            else:
                analysis = (
                    generate_satellite_interpretation(
                        evidence
                    )
                )

                st.session_state.satellite_evidence = (
                    evidence
                )
                st.session_state.satellite_analysis = (
                    analysis
                )

        evidence = (
            st.session_state.satellite_evidence
        )

        analysis = (
            st.session_state.satellite_analysis
        )

        if (
            evidence is not None
            and analysis is not None
        ):
            st.success(
                f"Regional analysis completed for "
                f"{evidence['region']}."
            )

            c1, c2, c3 = st.columns(3)

            c1.metric(
                "🧪 Mean HCHO",
                evidence["hcho_mean"],
            )

            c2.metric(
                "🌫 Mean Aerosol Index",
                evidence["aerosol_mean"],
            )

            c3.metric(
                "🔥 Fire Detection Pixels",
                evidence[
                    "fire_detection_pixels"
                ],
            )

            st.subheader(
                f"Evidence Level: "
                f"{analysis['level']}"
            )

            st.info(
                analysis["interpretation"]
            )

            if analysis["signals"]:
                st.write("**Signals detected:**")

                for signal in analysis["signals"]:
                    st.write(f"• {signal}")

            else:
                st.write(
                    "No prototype threshold signals "
                    "were detected."
                )

            with st.expander(
                "View observation details"
            ):
                st.write(
                    "HCHO images:",
                    evidence["hcho_image_count"],
                )

                st.write(
                    "Aerosol images:",
                    evidence[
                        "aerosol_image_count"
                    ],
                )

                st.write(
                    "FIRMS images:",
                    evidence[
                        "fire_image_count"
                    ],
                )

            st.caption(
                "The current thresholds are prototype "
                "decision rules, not validated scientific "
                "classification standards. AstraAir reports "
                "possible environmental influence and does "
                "not claim causation without ground "
                "validation."
            )

        st.divider()

        # ---------- Dataset explanation ----------

        if layer_name == "Sentinel-5P NO₂":
            st.subheader(
                "🧠 NO₂ Interpretation"
            )

            st.info(
                """
Higher NO₂ may be associated with:

- Road traffic emissions
- Industrial combustion
- Thermal power plants
- Biomass burning
"""
            )

        elif layer_name == "Sentinel-5P HCHO":
            st.subheader(
                "🧪 HCHO / Formaldehyde Interpretation"
            )

            st.info(
                """
Higher HCHO may be associated with:

- Biomass and crop-residue burning
- Volatile organic compound emissions
- Industrial chemical activity
- Wildfire and vegetation-related emissions
"""
            )

        elif layer_name == (
            "Sentinel-5P Aerosol Index"
        ):
            st.subheader(
                "🌫 Aerosol Index Interpretation"
            )

            st.info(
                """
Higher positive Aerosol Index values may indicate:

- Smoke from biomass or forest fires
- Desert dust
- Volcanic ash
- Other UV-absorbing aerosol plumes

The Aerosol Index is not a direct PM2.5 measurement.
"""
            )

        elif layer_name == (
            "NASA FIRMS Fire Hotspots"
        ):
            st.subheader(
                "🔥 Active Fire Interpretation"
            )

            st.warning(
                """
NASA FIRMS observations indicate active fire or
thermal-anomaly detections.

Possible sources may include:

- Crop-residue burning
- Forest or vegetation fires
- Biomass burning
- Other high-temperature thermal events

A hotspot does not by itself prove the cause of
regional air pollution.
"""
            )

    else:
        st.info(
            "Select a dataset and click "
            "**Load Satellite Data**."
        )