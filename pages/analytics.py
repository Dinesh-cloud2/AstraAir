import streamlit as st
import pandas as pd
import plotly.express as px

def analytics_page():

    st.title("📊 Environmental Analytics")

    df = pd.read_csv("data/cities.csv")

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

    st.subheader("AQI Pie Chart")

    pie = px.pie(
        df,
        names="City",
        values="AQI",
        title="AQI Contribution by City"
    )

    st.plotly_chart(pie, use_container_width=True)