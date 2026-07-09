import streamlit as st
import pandas as pd
from fpdf import FPDF
from pathlib import Path
from datetime import datetime

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


def reports_page():

    st.title("📄 Live Environmental Report Generator")

    df = pd.read_csv("data/cities.csv")

    city = st.selectbox("Select City", sorted(df["City"].unique()))

    row = df[df["City"] == city].iloc[0]

    air = get_live_aqi(row["Latitude"], row["Longitude"])
    weather = get_weather(city)

    if not air:
        st.error("Live AQI data not available.")
        return

    aqi = air["aqi"]
    label = get_aqi_label(aqi)
    advice = get_health_advice(aqi)

    st.subheader("Report Preview")

    c1, c2, c3 = st.columns(3)

    c1.metric("AQI Level", f"{aqi} ({label})")
    c2.metric("PM2.5", air["pm2_5"])
    c3.metric("PM10", air["pm10"])

    if weather:
        w1, w2, w3 = st.columns(3)
        w1.metric("Temperature", f"{weather['temperature']} °C")
        w2.metric("Humidity", f"{weather['humidity']} %")
        w3.metric("Wind", f"{weather['wind']} m/s")

    st.warning(advice)

    if st.button("Generate Live PDF Report"):

        Path("reports").mkdir(exist_ok=True)

        filename = f"reports/{city}_live_environment_report.pdf"

        pdf = FPDF()
        pdf.add_page()

        pdf.set_font("Arial", "B", 18)
        pdf.cell(200, 12, "AstraAir Environmental Intelligence Report", ln=True)

        pdf.set_font("Arial", size=11)
        pdf.cell(200, 8, f"Generated On: {datetime.now().strftime('%d-%m-%Y %H:%M')}", ln=True)
        pdf.cell(200, 8, f"City: {city}", ln=True)

        pdf.ln(6)

        pdf.set_font("Arial", "B", 14)
        pdf.cell(200, 10, "Live AQI Summary", ln=True)

        pdf.set_font("Arial", size=11)
        pdf.cell(200, 8, f"AQI Level: {aqi} ({label})", ln=True)
        pdf.cell(200, 8, f"PM2.5: {air['pm2_5']} ug/m3", ln=True)
        pdf.cell(200, 8, f"PM10: {air['pm10']} ug/m3", ln=True)
        pdf.cell(200, 8, f"NO2: {air['no2']} ug/m3", ln=True)
        pdf.cell(200, 8, f"O3: {air['o3']} ug/m3", ln=True)
        pdf.cell(200, 8, f"CO: {air['co']} ug/m3", ln=True)

        pdf.ln(6)

        pdf.set_font("Arial", "B", 14)
        pdf.cell(200, 10, "Live Weather Summary", ln=True)

        pdf.set_font("Arial", size=11)

        if weather:
            pdf.cell(200, 8, f"Temperature: {weather['temperature']} C", ln=True)
            pdf.cell(200, 8, f"Humidity: {weather['humidity']} %", ln=True)
            pdf.cell(200, 8, f"Wind Speed: {weather['wind']} m/s", ln=True)
            pdf.cell(200, 8, f"Condition: {weather['description']}", ln=True)
        else:
            pdf.cell(200, 8, "Weather data unavailable.", ln=True)

        pdf.ln(6)

        pdf.set_font("Arial", "B", 14)
        pdf.cell(200, 10, "Health Recommendation", ln=True)

        pdf.set_font("Arial", size=11)
        pdf.multi_cell(0, 8, advice)

        pdf.ln(6)

        pdf.set_font("Arial", "I", 10)
        pdf.multi_cell(
            0,
            8,
            "Note: AQI level is based on OpenWeather Air Pollution API scale from 1 Good to 5 Very Poor."
        )

        pdf.output(filename)

        st.success("Live PDF report generated successfully!")

        with open(filename, "rb") as file:
            st.download_button(
                "⬇ Download Live PDF Report",
                file,
                file_name=f"{city}_live_environment_report.pdf",
                mime="application/pdf"
            )