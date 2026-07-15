import folium
import streamlit as st
from streamlit_folium import folium_static

from services.aqi import get_live_aqi
from services.cities import get_cities

from utils.aqi_utils import (
    get_aqi_color,
    get_aqi_label,
    get_health_advice,
)


def map_page():

    st.title("🗺️ Live India AQI Map")

    st.caption(
        "Current AQI and pollutant observations from OpenWeather. "
        "Data is cached for 10 minutes."
    )

    # ==========================================
    # LOAD CITY DATA
    # ==========================================

    cities_df = get_cities()

    if cities_df.empty:
        st.error("City dataset is empty.")
        return

    # ==========================================
    # STATE FILTER
    # ==========================================

    state_options = [
        "All States"
    ] + sorted(
        cities_df["State"]
        .dropna()
        .unique()
        .tolist()
    )

    selected_state = st.selectbox(
        "📍 Select State",
        state_options,
    )

    if selected_state == "All States":

        st.info(
            "For faster loading, select one state. "
            "You can still load all cities if required."
        )

        max_cities = st.slider(
            "Maximum cities to load",
            min_value=5,
            max_value=len(cities_df),
            value=min(15, len(cities_df)),
            step=5,
        )

        filtered_df = cities_df.head(max_cities)

    else:

        filtered_df = cities_df[
            cities_df["State"] == selected_state
        ].copy()

    # ==========================================
    # CITY SELECTION
    # ==========================================

    if filtered_df.empty:
        st.warning(
            "No cities are available for the selected state."
        )
        return

    # ==========================================
    # REFRESH BUTTON
    # ==========================================
    if st.button(
        "🔄 Refresh Live AQI",
        type="primary",
        use_container_width=True,
    ):
        get_live_aqi.clear()
        st.rerun()

    # ==========================================
    # AQI SCALE
    # ==========================================

    with st.expander(
        "🌈 Understand OpenWeather AQI Scale",
        expanded=False,
    ):

        st.markdown(
            """
| AQI Level | Category | Meaning |
|---:|---|---|
| 1 | 🟢 Good | Air quality is good |
| 2 | 🔵 Fair | Air quality is acceptable |
| 3 | 🟡 Moderate | Sensitive groups should be cautious |
| 4 | 🟠 Poor | Reduce prolonged outdoor activity |
| 5 | 🔴 Very Poor | Avoid unnecessary outdoor exposure |

The AQI category is provided directly by the
OpenWeather Air Pollution API.

PM2.5, PM10, NO₂, O₃ and CO are shown separately
as current pollutant observations.
"""
        )

    st.write(
        f"Loading **{len(filtered_df)} cities**."
    )

    # ==========================================
    # CREATE MAP
    # ==========================================

    if selected_state == "All States":

        map_location = [22.5, 79.0]
        map_zoom = 5

    else:

        map_location = [
            filtered_df["Latitude"].mean(),
            filtered_df["Longitude"].mean(),
        ]

        map_zoom = 7

    india_map = folium.Map(
        location=map_location,
        zoom_start=map_zoom,
        tiles="CartoDB positron",
    )

    progress_bar = st.progress(0)
    progress_text = st.empty()

    total_cities = len(filtered_df)

    successful_aqi = 0
    unavailable_aqi = 0

    city_results = []

    # ==========================================
    # FETCH LIVE AQI
    # ==========================================

    for index, (_, row) in enumerate(
        filtered_df.iterrows(),
        start=1,
    ):

        city = row["City"]
        state = row["State"]

        latitude = float(row["Latitude"])
        longitude = float(row["Longitude"])

        progress_text.caption(
            f"Loading AQI: {city}, {state} "
            f"({index}/{total_cities})"
        )

        progress_bar.progress(
            index / total_cities
        )

        air = get_live_aqi(
            latitude,
            longitude,
        )

        if air:

            successful_aqi += 1

            aqi_level = air["aqi"]

            aqi_label = get_aqi_label(
                aqi_level
            )

            color = get_aqi_color(
                aqi_level
            )

            advice = get_health_advice(
                aqi_level
            )

            pm2_5 = air["pm2_5"]
            pm10 = air["pm10"]
            no2 = air["no2"]
            o3 = air["o3"]
            co = air["co"]

            popup_text = f"""
            <h4>{city}, {state}</h4>

            <b>OpenWeather AQI:</b>
            {aqi_level}/5 ({aqi_label})<br><br>

            <b>PM2.5:</b>
            {pm2_5} µg/m³<br>

            <b>PM10:</b>
            {pm10} µg/m³<br>

            <b>NO₂:</b>
            {no2} µg/m³<br>

            <b>O₃:</b>
            {o3} µg/m³<br>

            <b>CO:</b>
            {co} µg/m³<br><br>

            <b>Health Advice:</b><br>
            {advice}
            """

            city_results.append(
                {
                    "City": city,
                    "State": state,
                    "AQI Level": aqi_level,
                    "Category": aqi_label,
                    "PM2.5": pm2_5,
                    "PM10": pm10,
                    "NO2": no2,
                }
            )

        else:

            unavailable_aqi += 1

            aqi_level = "N/A"
            aqi_label = "Unavailable"
            color = "gray"

            popup_text = f"""
            <h4>{city}, {state}</h4>

            <b>AQI data is currently unavailable.</b>
            """

        popup = folium.Popup(
            popup_text,
            max_width=350,
        )

        folium.CircleMarker(
            location=[
                latitude,
                longitude,
            ],
            radius=9,
            popup=popup,
            tooltip=(
                f"{city}, {state} — "
                f"AQI {aqi_level} ({aqi_label})"
            ),
            color=color,
            weight=2,
            fill=True,
            fill_color=color,
            fill_opacity=0.8,
        ).add_to(india_map)

    progress_bar.empty()
    progress_text.empty()

    # ==========================================
    # METRICS
    # ==========================================

    metric1, metric2, metric3 = st.columns(3)

    metric1.metric(
        "📍 Cities Loaded",
        total_cities,
    )

    metric2.metric(
        "✅ AQI Available",
        successful_aqi,
    )

    metric3.metric(
        "⚠️ AQI Unavailable",
        unavailable_aqi,
    )

    # ==========================================
    # DISPLAY MAP
    # ==========================================

    folium_static(
        india_map,
        width=1200,
        height=700,
    )

    # ==========================================
    # CITY DATA TABLE
    # ==========================================

    if city_results:

        st.subheader(
            "📊 Live City AQI Summary"
        )

        st.dataframe(
            city_results,
            use_container_width=True,
            hide_index=True,
        )

    st.caption(
        "The displayed AQI category uses the OpenWeather "
        "1–5 scale. Pollutant concentrations are current API "
        "observations and may differ from official CPCB "
        "monitoring-station values."
    )