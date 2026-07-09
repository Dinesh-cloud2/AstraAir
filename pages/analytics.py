import streamlit as st
import pandas as pd
import plotly.express as px


def analytics_page():

    st.title("📊 Environmental Analytics")

    df = pd.read_csv("data/cities.csv")

    st.sidebar.subheader("📊 Analytics Filter")

    selected_city = st.sidebar.selectbox(
        "Select City",
        ["All"] + sorted(df["City"].unique().tolist())
    )

    if selected_city != "All":
        df = df[df["City"] == selected_city]

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("🌍 Cities", len(df))
    c2.metric("📈 Average AQI", round(df["AQI"].mean()))
    c3.metric("🚨 Highest AQI", df["AQI"].max())
    c4.metric("😊 Lowest AQI", df["AQI"].min())

    st.success(f"""
### 🌍 Environmental Summary

📍 Total Cities Monitored: **{len(df)}**

🚨 Highest AQI: **{df['AQI'].max()}**

😊 Lowest AQI: **{df['AQI'].min()}**

📈 Average AQI: **{round(df['AQI'].mean())}**
""")

    highest = df.loc[df["AQI"].idxmax()]
    lowest = df.loc[df["AQI"].idxmin()]

    col1, col2 = st.columns(2)

    with col1:
        st.warning(f"""
### 🚨 Most Polluted City

🏙️ {highest['City']}

AQI: {highest['AQI']}
""")

    with col2:
        st.success(f"""
### 🌿 Cleanest City

🏙️ {lowest['City']}

AQI: {lowest['AQI']}
""")

    score = max(0, 100 - round(df["AQI"].mean() / 2))
    st.metric("🌎 Environmental Health Score", f"{score}/100")

    st.divider()

    fig = px.bar(
        df,
        x="City",
        y="AQI",
        color="AQI",
        color_continuous_scale="RdYlGn_r",
        title="AQI Across Cities"
    )
    st.plotly_chart(fig, use_container_width=True)

    trend = px.line(
        df,
        x="City",
        y="AQI",
        markers=True,
        title="AQI Trend"
    )
    st.plotly_chart(trend, use_container_width=True)

    temp_fig = px.bar(
        df,
        x="City",
        y="Temperature",
        color="Temperature",
        title="Temperature Across Cities"
    )
    st.plotly_chart(temp_fig, use_container_width=True)

    humidity_fig = px.bar(
        df,
        x="City",
        y="Humidity",
        color="Humidity",
        title="Humidity Across Cities"
    )
    st.plotly_chart(humidity_fig, use_container_width=True)

    wind_fig = px.bar(
        df,
        x="City",
        y="Wind",
        color="Wind",
        title="Wind Speed Across Cities"
    )
    st.plotly_chart(wind_fig, use_container_width=True)

    st.divider()

    st.subheader("🚨 Top 5 Polluted Cities")
    top5 = df.sort_values("AQI", ascending=False).head(5)
    st.dataframe(top5, use_container_width=True)

    st.subheader("🌿 Cleanest Cities")
    clean = df.sort_values("AQI").head(5)
    st.dataframe(clean, use_container_width=True)

    st.divider()

    pie = px.pie(
        df,
        names="City",
        values="AQI",
        title="AQI Contribution by City"
    )
    st.plotly_chart(pie, use_container_width=True)

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

    category_fig = px.histogram(
        df,
        x="Category",
        color="Category",
        title="AQI Category Distribution"
    )
    st.plotly_chart(category_fig, use_container_width=True)

    st.divider()

    st.download_button(
        "📥 Download Analytics CSV",
        data=df.to_csv(index=False),
        file_name="astraair_analytics.csv",
        mime="text/csv"
    )