import streamlit as st
import pandas as pd
import plotly.express as px

from services.aqi import get_live_aqi


def get_aqi_label(aqi):
    labels = {
        1: "Good",
        2: "Fair",
        3: "Moderate",
        4: "Poor",
        5: "Very Poor"
    }
    return labels.get(aqi, "Unknown")


def analytics_page():

    st.title("📊 Live Environmental Analytics")

    df = pd.read_csv("data/cities.csv")

    live_rows = []

    for _, row in df.iterrows():
        air = get_live_aqi(row["Latitude"], row["Longitude"])

        if air:
            live_rows.append({
                "City": row["City"],
                "Latitude": row["Latitude"],
                "Longitude": row["Longitude"],
                "AQI": air["aqi"],
                "AQI_Label": get_aqi_label(air["aqi"]),
                "PM2.5": air["pm2_5"],
                "PM10": air["pm10"],
                "NO2": air["no2"],
                "O3": air["o3"],
                "CO": air["co"],
                "Temperature": row["Temperature"],
                "Humidity": row["Humidity"],
                "Wind": row["Wind"]
            })

    live_df = pd.DataFrame(live_rows)

    if live_df.empty:
        st.error("Live AQI data not available.")
        return

    selected_city = st.sidebar.selectbox(
        "Select City",
        ["All"] + sorted(live_df["City"].unique().tolist())
    )

    if selected_city != "All":
        live_df = live_df[live_df["City"] == selected_city]

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("🌍 Cities", len(live_df))
    c2.metric("📈 Avg AQI Level", round(live_df["AQI"].mean(), 2))
    c3.metric("🚨 Highest AQI Level", live_df["AQI"].max())
    c4.metric("😊 Lowest AQI Level", live_df["AQI"].min())

    st.divider()

    fig = px.bar(
        live_df,
        x="City",
        y="AQI",
        color="AQI",
        color_continuous_scale="RdYlGn_r",
        title="Live AQI Level Across Cities"
    )
    st.plotly_chart(fig, use_container_width=True)

    pollutant_fig = px.bar(
        live_df,
        x="City",
        y=["PM2.5", "PM10", "NO2", "O3"],
        title="Live Pollutant Comparison"
    )
    st.plotly_chart(pollutant_fig, use_container_width=True)

    st.subheader("🚨 Top Polluted Cities")
    st.dataframe(
        live_df.sort_values("AQI", ascending=False).head(5),
        use_container_width=True
    )

    st.subheader("🌿 Cleanest Cities")
    st.dataframe(
        live_df.sort_values("AQI").head(5),
        use_container_width=True
    )

    st.divider()

    pie = px.pie(
        live_df,
        names="AQI_Label",
        title="AQI Category Distribution"
    )
    st.plotly_chart(pie, use_container_width=True)

    st.download_button(
        "📥 Download Live Analytics CSV",
        data=live_df.to_csv(index=False),
        file_name="astraair_live_analytics.csv",
        mime="text/csv"
    )