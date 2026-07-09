import streamlit as st
import pandas as pd
from fpdf import FPDF
from pathlib import Path


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


def reports_page():

    st.title("📄 Environmental Report Generator")

    df = pd.read_csv("data/cities.csv")

    city = st.selectbox(
        "Select City",
        sorted(df["City"].unique())
    )

    row = df[df["City"] == city].iloc[0]

    st.subheader("Report Preview")

    st.write(f"**City:** {row['City']}")
    st.write(f"**AQI:** {row['AQI']}")
    st.write(f"**Temperature:** {row['Temperature']} °C")
    st.write(f"**Humidity:** {row['Humidity']} %")
    st.write(f"**Wind Speed:** {row['Wind']} m/s")
    st.write(f"**Health Advice:** {get_health_advice(row['AQI'])}")

    if st.button("Generate PDF Report"):

        Path("reports").mkdir(exist_ok=True)

        filename = f"reports/{city}_environment_report.pdf"

        pdf = FPDF()
        pdf.add_page()

        pdf.set_font("Arial", size=16)
        pdf.cell(200, 10, "AstraAir Environmental Report", ln=True)

        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, f"City: {row['City']}", ln=True)
        pdf.cell(200, 10, f"AQI: {row['AQI']}", ln=True)
        pdf.cell(200, 10, f"Temperature: {row['Temperature']} C", ln=True)
        pdf.cell(200, 10, f"Humidity: {row['Humidity']} %", ln=True)
        pdf.cell(200, 10, f"Wind Speed: {row['Wind']} m/s", ln=True)
        pdf.cell(200, 10, f"Health Advice: {get_health_advice(row['AQI'])}", ln=True)

        pdf.output(filename)

        st.success("PDF report generated successfully!")

        with open(filename, "rb") as file:
            st.download_button(
                "⬇ Download PDF Report",
                file,
                file_name=f"{city}_environment_report.pdf",
                mime="application/pdf"
            )