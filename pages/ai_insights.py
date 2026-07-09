import streamlit as st
import pandas as pd


def get_risk_level(aqi):
    if aqi <= 50:
        return "🟢 Low Risk"
    elif aqi <= 100:
        return "🟡 Moderate Risk"
    elif aqi <= 150:
        return "🟠 Unhealthy for Sensitive Groups"
    elif aqi <= 200:
        return "🔴 High Risk"
    else:
        return "🚨 Severe Risk"


def get_ai_reason(row):
    reasons = []

    if row["AQI"] > 150:
        reasons.append("High AQI indicates poor air quality.")

    if row["Temperature"] > 32:
        reasons.append("High temperature may increase pollution formation.")

    if row["Humidity"] > 75:
        reasons.append("High humidity can trap pollutants near the surface.")

    if row["Wind"] < 3:
        reasons.append("Low wind speed reduces pollution dispersion.")

    if not reasons:
        reasons.append("Environmental conditions are currently stable.")

    return reasons


def get_health_advice(aqi):
    if aqi <= 50:
        return "Air quality is good. Outdoor activities are safe."
    elif aqi <= 100:
        return "Moderate air quality. Sensitive people should take care."
    elif aqi <= 150:
        return "Reduce long outdoor activity if you are sensitive."
    elif aqi <= 200:
        return "Wear a mask outdoors and avoid heavy exercise."
    else:
        return "Avoid outdoor exposure. Children and elderly should stay indoors."


def predict_tomorrow_aqi(row):
    predicted = row["AQI"]

    if row["Wind"] < 3:
        predicted += 8

    if row["Temperature"] > 32:
        predicted += 6

    if row["Humidity"] > 75:
        predicted += 5

    return round(predicted)


def ai_insights_page():

    st.title("🤖 AI Environmental Insights")

    df = pd.read_csv("data/cities.csv")

    city = st.selectbox(
        "Select City",
        sorted(df["City"].unique())
    )

    row = df[df["City"] == city].iloc[0]

    predicted_aqi = predict_tomorrow_aqi(row)
    risk = get_risk_level(row["AQI"])
    advice = get_health_advice(row["AQI"])
    reasons = get_ai_reason(row)

    c1, c2, c3 = st.columns(3)

    c1.metric("Current AQI", row["AQI"])
    c2.metric("Predicted Tomorrow", predicted_aqi)
    c3.metric("Risk Level", risk)

    st.divider()

    st.subheader("🧠 Why is AQI like this?")

    for reason in reasons:
        st.write(f"✅ {reason}")

    st.divider()

    st.subheader("🏥 Health Recommendation")
    st.warning(advice)

    st.divider()

    st.subheader("📊 Environmental Factors")

    st.write(f"🌡 Temperature: **{row['Temperature']} °C**")
    st.write(f"💧 Humidity: **{row['Humidity']} %**")
    st.write(f"🌬 Wind Speed: **{row['Wind']} m/s**")

    st.info("AI Insight is rule-based for now. Later we will replace it with a trained ML model + SHAP explainability.")