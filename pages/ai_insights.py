import streamlit as st
import pandas as pd

from services.aqi import get_live_aqi
from services.weather import get_weather


def get_aqi_label(aqi):
    labels = {
        1: "Good",
        2: "Fair",
        3: "Moderate",
        4: "Poor",
        5: "Very Poor"
    }
    return labels.get(aqi, "Unknown")


def get_risk_level(aqi):
    if aqi == 1:
        return "🟢 Low Risk"
    elif aqi == 2:
        return "🟡 Mild Risk"
    elif aqi == 3:
        return "🟠 Moderate Risk"
    elif aqi == 4:
        return "🔴 High Risk"
    else:
        return "🚨 Severe Risk"


def get_health_advice(aqi):
    if aqi == 1:
        return "Air quality is good. Outdoor activities are safe."
    elif aqi == 2:
        return "Air quality is fair. Most people can continue normal activity."
    elif aqi == 3:
        return "Moderate pollution. Sensitive people should reduce long outdoor activity."
    elif aqi == 4:
        return "Poor air quality. Wear a mask outdoors and avoid heavy exercise."
    else:
        return "Very poor air quality. Avoid outdoor exposure. Children and elderly should stay indoors."


def predict_tomorrow_aqi(aqi, weather):
    predicted = aqi

    if weather:
        if weather["wind"] < 3:
            predicted += 1
        if weather["humidity"] > 75:
            predicted += 1
        if weather["temperature"] > 35:
            predicted += 1

    return min(predicted, 5)


def ai_reasons(air, weather):
    reasons = []

    if air["pm2_5"] > 25:
        reasons.append("PM2.5 is elevated, which can increase respiratory health risk.")

    if air["pm10"] > 50:
        reasons.append("PM10 levels are high, indicating dust or coarse particles.")

    if air["no2"] > 40:
        reasons.append("NO₂ is high, which may indicate traffic or combustion emissions.")

    if weather:
        if weather["wind"] < 3:
            reasons.append("Low wind speed can reduce pollutant dispersion.")
        if weather["humidity"] > 75:
            reasons.append("High humidity can keep pollutants near the surface.")

    if not reasons:
        reasons.append("Current environmental conditions appear stable.")

    return reasons


def ai_insights_page():

    st.title("🤖 Live AI Environmental Insights")

    df = pd.read_csv("data/cities.csv")

    city = st.selectbox(
        "Select City",
        sorted(df["City"].unique())
    )

    row = df[df["City"] == city].iloc[0]

    air = get_live_aqi(row["Latitude"], row["Longitude"])
    weather = get_weather(city)

    if not air:
        st.error("Live AQI data not available.")
        return

    aqi = air["aqi"]
    label = get_aqi_label(aqi)
    risk = get_risk_level(aqi)
    predicted = predict_tomorrow_aqi(aqi, weather)

    c1, c2, c3 = st.columns(3)

    c1.metric("Current AQI Level", f"{aqi} ({label})")
    c2.metric("Predicted Tomorrow", f"{predicted} ({get_aqi_label(predicted)})")
    c3.metric("Risk Level", risk)

    st.divider()

    st.subheader("🌫 Live Pollutant Data")

    p1, p2, p3, p4, p5 = st.columns(5)

    p1.metric("PM2.5", air["pm2_5"])
    p2.metric("PM10", air["pm10"])
    p3.metric("NO₂", air["no2"])
    p4.metric("O₃", air["o3"])
    p5.metric("CO", air["co"])

    st.divider()

    st.subheader("🌦 Live Weather Conditions")

    if weather:
        w1, w2, w3 = st.columns(3)
        w1.metric("Temperature", f"{weather['temperature']} °C")
        w2.metric("Humidity", f"{weather['humidity']} %")
        w3.metric("Wind", f"{weather['wind']} m/s")
    else:
        st.warning("Weather data not available.")

    st.divider()

    st.subheader("🧠 AI Explanation")

    for reason in ai_reasons(air, weather):
        st.write(f"✅ {reason}")

    st.divider()

    st.subheader("🏥 Health Recommendation")
    st.warning(get_health_advice(aqi))

    st.info("This AI insight is rule-based for now. Later we will add ML + SHAP explainability.")