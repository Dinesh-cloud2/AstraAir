import streamlit as st
import pandas as pd
import plotly.express as px


def analytics_page():

    st.title("📊 Environmental Analytics")

    df = pd.read_csv("data/cities.csv")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("🌍 Cities", len(df))
    c2.metric("📈 Average AQI", round(df["AQI"].mean()))
    c3.metric("🚨 Highest AQI", df["AQI"].max())
    c4.metric("😊 Lowest AQI", df["AQI"].min())

    st.divider()

    st.subheader("AQI Distribution")

    fig = px.bar(
        df,
        x="City",
        y="AQI",
        color="AQI",
        color_continuous_scale="RdYlGn_r",
        title="AQI Across Indian Cities"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    st.subheader("🚨 Top 5 Polluted Cities")

    top5 = df.sort_values("AQI", ascending=False).head(5)
    st.dataframe(top5, use_container_width=True)

    st.subheader("🌿 Cleanest Cities")

    clean = df.sort_values("AQI").head(5)
    st.dataframe(clean, use_container_width=True)

    st.divider()

    st.subheader("AQI Pie Chart")

    pie = px.pie(
        df,
        names="City",
        values="AQI",
        title="AQI Contribution by City"
    )

    st.plotly_chart(pie, use_container_width=True)

    st.divider()

    def category(aqi):
        if aqi <= 50:
            return "Good"
        elif aqi <= 100:
            return "Moderate"
        elif aqi <= 150:
            return "Unhealthy"
        else:
            return "Very Poor"

    df["Category"] = df["AQI"].apply(category)

    st.subheader("AQI Category Distribution")

    category_fig = px.histogram(
        df,
        x="Category",
        color="Category",
        title="AQI Categories"
    )

    st.plotly_chart(category_fig, use_container_width=True)