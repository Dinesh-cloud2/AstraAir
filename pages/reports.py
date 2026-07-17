from datetime import datetime

import streamlit as st
from fpdf import FPDF

from services.aqi import get_live_aqi
from services.cities import get_cities
from services.weather import get_weather

from utils.aqi_utils import (
    get_aqi_label,
    get_health_advice,
    get_risk_level,
)


def clean_pdf_text(text):
    replacements = {
        "🟢": "",
        "🟡": "",
        "🟠": "",
        "🔴": "",
        "🚨": "",
        "🌫": "",
        "🌦": "",
        "🏥": "",
        "📄": "",
        "µ": "u",
        "³": "3",
        "₂": "2",
        "₃": "3",
        "–": "-",
        "—": "-",
        "→": "to",
    }

    text = str(text)

    for old, new in replacements.items():
        text = text.replace(old, new)

    return text.strip()


def create_environment_report(
    city,
    state,
    air,
    weather,
):
    aqi_level = air["aqi"]

    aqi_label = clean_pdf_text(
        get_aqi_label(aqi_level)
    )

    risk_level = clean_pdf_text(
        get_risk_level(aqi_level)
    )

    advice = clean_pdf_text(
        get_health_advice(aqi_level)
    )

    pdf = FPDF()

    pdf.add_page()

    pdf.set_auto_page_break(
        auto=True,
        margin=15,
    )

    # ==========================================
    # REPORT TITLE
    # ==========================================

    pdf.set_font(
        "Arial",
        "B",
        18,
    )

    pdf.multi_cell(
        0,
        10,
        "AstraAir Environmental Intelligence Report",
    )

    pdf.ln(3)

    pdf.set_font(
        "Arial",
        size=11,
    )

    generated_time = datetime.now().strftime(
        "%d-%m-%Y %H:%M"
    )

    pdf.cell(
        0,
        8,
        clean_pdf_text(
            f"Generated On: {generated_time}"
        ),
        new_x="LMARGIN",
        new_y="NEXT",
    )

    pdf.cell(
        0,
        8,
        clean_pdf_text(
            f"Location: {city}, {state}"
        ),
        new_x="LMARGIN",
        new_y="NEXT",
    )

    pdf.ln(5)

    # ==========================================
    # AIR QUALITY SECTION
    # ==========================================

    pdf.set_font(
        "Arial",
        "B",
        14,
    )

    pdf.cell(
        0,
        10,
        "Current Air Quality Summary",
        new_x="LMARGIN",
        new_y="NEXT",
    )

    pdf.set_font(
        "Arial",
        size=11,
    )

    pdf.cell(
        0,
        8,
        clean_pdf_text(
            f"OpenWeather AQI Level: {aqi_level}/5"
        ),
        new_x="LMARGIN",
        new_y="NEXT",
    )

    pdf.cell(
        0,
        8,
        clean_pdf_text(
            f"AQI Category: {aqi_label}"
        ),
        new_x="LMARGIN",
        new_y="NEXT",
    )

    pdf.cell(
        0,
        8,
        clean_pdf_text(
            f"Risk Level: {risk_level}"
        ),
        new_x="LMARGIN",
        new_y="NEXT",
    )

    pdf.cell(
        0,
        8,
        clean_pdf_text(
            f"PM2.5: {air['pm2_5']} ug/m3"
        ),
        new_x="LMARGIN",
        new_y="NEXT",
    )

    pdf.cell(
        0,
        8,
        clean_pdf_text(
            f"PM10: {air['pm10']} ug/m3"
        ),
        new_x="LMARGIN",
        new_y="NEXT",
    )

    pdf.cell(
        0,
        8,
        clean_pdf_text(
            f"NO2: {air['no2']} ug/m3"
        ),
        new_x="LMARGIN",
        new_y="NEXT",
    )

    pdf.cell(
        0,
        8,
        clean_pdf_text(
            f"O3: {air['o3']} ug/m3"
        ),
        new_x="LMARGIN",
        new_y="NEXT",
    )

    pdf.cell(
        0,
        8,
        clean_pdf_text(
            f"CO: {air['co']} ug/m3"
        ),
        new_x="LMARGIN",
        new_y="NEXT",
    )

    pdf.ln(5)

    # ==========================================
    # WEATHER SECTION
    # ==========================================

    pdf.set_font(
        "Arial",
        "B",
        14,
    )

    pdf.cell(
        0,
        10,
        "Current Weather Summary",
        new_x="LMARGIN",
        new_y="NEXT",
    )

    pdf.set_font(
        "Arial",
        size=11,
    )

    if weather:

        pdf.cell(
            0,
            8,
            clean_pdf_text(
                f"Temperature: "
                f"{weather['temperature']} C"
            ),
            new_x="LMARGIN",
            new_y="NEXT",
        )

        pdf.cell(
            0,
            8,
            clean_pdf_text(
                f"Humidity: "
                f"{weather['humidity']} %"
            ),
            new_x="LMARGIN",
            new_y="NEXT",
        )

        pdf.cell(
            0,
            8,
            clean_pdf_text(
                f"Wind Speed: "
                f"{weather['wind']} m/s"
            ),
            new_x="LMARGIN",
            new_y="NEXT",
        )

        pdf.cell(
            0,
            8,
            clean_pdf_text(
                f"Condition: "
                f"{weather['description']}"
            ),
            new_x="LMARGIN",
            new_y="NEXT",
        )

    else:

        pdf.cell(
            0,
            8,
            "Weather data unavailable.",
            new_x="LMARGIN",
            new_y="NEXT",
        )

    pdf.ln(5)

    # ==========================================
    # HEALTH RECOMMENDATION
    # ==========================================

    pdf.set_font(
        "Arial",
        "B",
        14,
    )

    pdf.cell(
        0,
        10,
        "Health Recommendation",
        new_x="LMARGIN",
        new_y="NEXT",
    )

    pdf.set_font(
        "Arial",
        size=11,
    )

    pdf.multi_cell(
        0,
        8,
        advice,
    )

    pdf.ln(5)

    # ==========================================
    # DISCLAIMER
    # ==========================================

    pdf.set_font(
        "Arial",
        "I",
        9,
    )

    disclaimer = (
        "Note: The AQI category uses the OpenWeather "
        "Air Pollution API scale from 1 Good to "
        "5 Very Poor. Pollutant values are current "
        "API observations and may differ from official "
        "CPCB monitoring-station measurements."
    )

    pdf.multi_cell(
        0,
        7,
        clean_pdf_text(disclaimer),
    )

    pdf_bytes = pdf.output()

    if isinstance(pdf_bytes, str):
        pdf_bytes = pdf_bytes.encode(
            "latin-1"
        )

    return bytes(pdf_bytes)


def reports_page():

    st.title(
        "📄 Live Environmental Report Generator"
    )

    st.caption(
        "Generate a downloadable environmental report "
        "using current AQI, pollutant and weather data."
    )

    # ==========================================
    # LOAD SHARED CITY DATASET
    # ==========================================

    cities_df = get_cities()

    if cities_df.empty:
        st.error(
            "City dataset is empty."
        )
        return

    city_options = cities_df.apply(
        lambda row: (
            f"{row['City']}, {row['State']}"
        ),
        axis=1,
    ).tolist()

    selected_option = st.selectbox(
        "📍 Select City",
        city_options,
    )

    selected_row = cities_df[
        cities_df.apply(
            lambda row: (
                f"{row['City']}, {row['State']}"
                == selected_option
            ),
            axis=1,
        )
    ].iloc[0]

    city = selected_row["City"]
    state = selected_row["State"]

    latitude = float(
        selected_row["Latitude"]
    )

    longitude = float(
        selected_row["Longitude"]
    )

    # ==========================================
    # REFRESH BUTTON
    # ==========================================

    if st.button(
        "🔄 Refresh Report Data",
        use_container_width=True,
    ):

        get_live_aqi.clear()
        get_weather.clear()

        st.rerun()

    # ==========================================
    # FETCH LIVE DATA
    # ==========================================

    with st.spinner(
        f"Loading live environmental data for "
        f"{city}, {state}..."
    ):

        air = get_live_aqi(
            latitude,
            longitude,
        )

        weather = get_weather(
            city=city,
            lat=latitude,
            lon=longitude,
        )

    if not air:

        st.error(
            "Live AQI data is currently unavailable."
        )

        return

    aqi_level = air["aqi"]

    aqi_label = get_aqi_label(
        aqi_level
    )

    risk_level = get_risk_level(
        aqi_level
    )

    # ==========================================
    # REPORT PREVIEW
    # ==========================================

    st.subheader(
        "Report Preview"
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "AQI Level",
        f"{aqi_level}/5",
    )

    c2.metric(
        "Category",
        aqi_label,
    )

    c3.metric(
        "Risk Level",
        risk_level,
    )

    c4.metric(
        "Location",
        city,
    )

    st.divider()

    p1, p2, p3, p4, p5 = st.columns(5)

    p1.metric(
        "PM2.5",
        f"{air['pm2_5']} µg/m³",
    )

    p2.metric(
        "PM10",
        f"{air['pm10']} µg/m³",
    )

    p3.metric(
        "NO₂",
        f"{air['no2']} µg/m³",
    )

    p4.metric(
        "O₃",
        f"{air['o3']} µg/m³",
    )

    p5.metric(
        "CO",
        f"{air['co']} µg/m³",
    )

    # ==========================================
    # WEATHER PREVIEW
    # ==========================================

    if weather:

        st.divider()

        st.subheader(
            "Current Weather"
        )

        w1, w2, w3, w4 = st.columns(4)

        w1.metric(
            "Temperature",
            f"{weather['temperature']} °C",
        )

        w2.metric(
            "Humidity",
            f"{weather['humidity']} %",
        )

        w3.metric(
            "Wind",
            f"{weather['wind']} m/s",
        )

        w4.metric(
            "Condition",
            weather["description"],
        )

    else:

        st.warning(
            "Weather data is currently unavailable."
        )

    # ==========================================
    # HEALTH RECOMMENDATION
    # ==========================================

    st.divider()

    st.subheader(
        "🏥 Health Recommendation"
    )

    st.warning(
        get_health_advice(
            aqi_level
        )
    )

    # ==========================================
    # GENERATE PDF
    # ==========================================

    try:

        pdf_data = create_environment_report(
            city=city,
            state=state,
            air=air,
            weather=weather,
        )

    except Exception as error:

        st.error(
            "PDF report could not be generated."
        )

        st.code(
            str(error)
        )

        return

    safe_city_name = (
        str(city)
        .lower()
        .replace(" ", "_")
    )

    st.download_button(
        "⬇️ Download Live PDF Report",
        data=pdf_data,
        file_name=(
            f"{safe_city_name}_"
            f"environment_report.pdf"
        ),
        mime="application/pdf",
        type="primary",
        use_container_width=True,
    )

    st.caption(
        "This report uses current OpenWeather "
        "observations. It is not an official CPCB "
        "monitoring or medical report."
    )