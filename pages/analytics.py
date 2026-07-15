import pandas as pd
import plotly.express as px
import streamlit as st

from services.aqi import get_live_aqi
from services.cities import get_cities
from utils.aqi_utils import get_aqi_label


def analytics_page():

    st.title("📊 Live Environmental Analytics")

    st.caption(
        "Current AQI and pollutant observations from OpenWeather. "
        "Results are cached for 10 minutes."
    )

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

        max_cities = st.slider(
            "Maximum cities to analyze",
            min_value=5,
            max_value=len(cities_df),
            value=min(15, len(cities_df)),
            step=5,
        )

        filtered_cities = cities_df.head(
            max_cities
        ).copy()

        st.info(
            "All States mode uses a city limit for faster loading."
        )

    else:

        filtered_cities = cities_df[
            cities_df["State"] == selected_state
        ].copy()

    if filtered_cities.empty:
        st.warning(
            "No cities are available for the selected state."
        )
        return

    # ==========================================
    # REFRESH BUTTON
    # ==========================================

    if st.button(
        "🔄 Refresh Live Analytics",
        type="primary",
        use_container_width=True,
    ):
        get_live_aqi.clear()
        st.rerun()

    st.write(
        f"Analyzing **{len(filtered_cities)} cities**."
    )

    # ==========================================
    # FETCH LIVE DATA
    # ==========================================

    live_rows = []

    progress = st.progress(0)
    status = st.empty()

    total_cities = len(filtered_cities)

    for index, (_, row) in enumerate(
        filtered_cities.iterrows(),
        start=1,
    ):

        city = row["City"]
        state = row["State"]

        latitude = float(row["Latitude"])
        longitude = float(row["Longitude"])

        status.caption(
            f"Loading AQI: {city}, {state} "
            f"({index}/{total_cities})"
        )

        progress.progress(
            index / total_cities
        )

        air = get_live_aqi(
            latitude,
            longitude,
        )

        if not air:
            continue

        aqi_level = air["aqi"]

        live_rows.append(
            {
                "City": city,
                "State": state,
                "AQI_Level": aqi_level,
                "AQI_Category": get_aqi_label(
                    aqi_level
                ),
                "PM2.5": air["pm2_5"],
                "PM10": air["pm10"],
                "NO2": air["no2"],
                "O3": air["o3"],
                "CO": air["co"],
            }
        )

    progress.empty()
    status.empty()

    live_df = pd.DataFrame(
        live_rows
    )

    if live_df.empty:
        st.error(
            "Live analytics data could not be loaded."
        )
        return

    # ==========================================
    # KPI METRICS
    # ==========================================

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "📍 Cities",
        len(live_df),
    )

    c2.metric(
        "📈 Average AQI Level",
        round(
            live_df["AQI_Level"].mean(),
            1,
        ),
    )

    c3.metric(
        "🚨 Highest AQI Level",
        int(
            live_df["AQI_Level"].max()
        ),
    )

    c4.metric(
        "🌿 Lowest AQI Level",
        int(
            live_df["AQI_Level"].min()
        ),
    )

    st.divider()

    # ==========================================
    # AQI LEVEL CHART
    # ==========================================

    st.subheader(
        "📊 AQI Level Across Cities"
    )

    aqi_fig = px.bar(
        live_df.sort_values(
            "AQI_Level",
            ascending=False,
        ),
        x="City",
        y="AQI_Level",
        color="AQI_Level",
        hover_data=[
            "State",
            "AQI_Category",
            "PM2.5",
            "PM10",
        ],
        color_continuous_scale="RdYlGn_r",
        title="Current OpenWeather AQI Level",
    )

    aqi_fig.update_yaxes(
        range=[0, 5.5],
        dtick=1,
    )

    st.plotly_chart(
        aqi_fig,
        use_container_width=True,
    )

    st.caption(
        "OpenWeather AQI scale: "
        "1 Good, 2 Fair, 3 Moderate, "
        "4 Poor, 5 Very Poor."
    )

    st.divider()

    # ==========================================
    # POLLUTANT COMPARISON
    # ==========================================

    st.subheader(
        "🌫 Pollutant Comparison"
    )

    pollutant_fig = px.bar(
        live_df,
        x="City",
        y=[
            "PM2.5",
            "PM10",
            "NO2",
            "O3",
        ],
        barmode="group",
        title="Current Pollutant Concentrations",
    )

    st.plotly_chart(
        pollutant_fig,
        use_container_width=True,
    )

    st.divider()

    # ==========================================
    # RANKINGS
    # ==========================================

    st.subheader(
        "🚨 Highest Pollution Observations"
    )

    highest = (
        live_df
        .sort_values(
            [
                "AQI_Level",
                "PM2.5",
            ],
            ascending=False,
        )
        .head(5)
    )

    st.dataframe(
        highest[
            [
                "City",
                "State",
                "AQI_Level",
                "AQI_Category",
                "PM2.5",
                "PM10",
                "NO2",
            ]
        ],
        use_container_width=True,
        hide_index=True,
    )

    st.subheader(
        "🌿 Lowest Pollution Observations"
    )

    lowest = (
        live_df
        .sort_values(
            [
                "AQI_Level",
                "PM2.5",
            ],
            ascending=True,
        )
        .head(5)
    )

    st.dataframe(
        lowest[
            [
                "City",
                "State",
                "AQI_Level",
                "AQI_Category",
                "PM2.5",
                "PM10",
                "NO2",
            ]
        ],
        use_container_width=True,
        hide_index=True,
    )

    st.divider()

    # ==========================================
    # CATEGORY DISTRIBUTION
    # ==========================================

    st.subheader(
        "🏷 AQI Category Distribution"
    )

    category_counts = (
        live_df["AQI_Category"]
        .value_counts()
        .reset_index()
    )

    category_counts.columns = [
        "AQI Category",
        "Cities",
    ]

    category_fig = px.bar(
        category_counts,
        x="AQI Category",
        y="Cities",
        color="AQI Category",
        title="Cities by AQI Category",
    )

    st.plotly_chart(
        category_fig,
        use_container_width=True,
    )

    st.divider()

    # ==========================================
    # DATA TABLE
    # ==========================================

    with st.expander(
        "📂 View Complete Live Dataset"
    ):

        st.dataframe(
            live_df,
            use_container_width=True,
            hide_index=True,
        )

    st.download_button(
        "📥 Download Live Analytics CSV",
        data=live_df.to_csv(
            index=False
        ),
        file_name=(
            "astraair_live_pollution_analytics.csv"
        ),
        mime="text/csv",
    )

    st.caption(
        "AQI uses the OpenWeather 1–5 scale. "
        "Pollutant values are current API observations "
        "and may differ from official CPCB station data."
    )