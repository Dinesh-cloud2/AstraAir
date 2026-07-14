import streamlit as st


def about_page():

    st.title("🛰️ About AstraAir")

    st.markdown("""
# AstraAir

**From Space to Smarter Air**

AstraAir is a satellite-powered Environmental Intelligence Platform that combines Earth observation, live air-quality data, weather information, analytics, and explainable environmental insights.

---

## 🎯 Project Vision

The goal of AstraAir is to make environmental data easier to understand and more useful for decision-making.

The platform is designed to answer questions such as:

- What is the current air-quality condition?
- Which pollutants are elevated?
- What do satellite observations show?
- Are fire, aerosol, or formaldehyde signals present?
- How may weather affect pollution dispersion?
- What health precautions should people take?

---

## 🛰️ Satellite Intelligence

AstraAir uses Google Earth Engine to process environmental satellite observations.

Current satellite datasets include:

- Sentinel-5P NO₂
- Sentinel-5P HCHO / Formaldehyde
- Sentinel-5P Absorbing Aerosol Index
- NASA FIRMS active-fire and thermal-anomaly observations

The platform supports date selection, regional analysis, interactive maps, satellite evidence interpretation, and environmental data fusion.

---

## 🌍 Live Environmental Data

AstraAir integrates live data from OpenWeather:

- Temperature
- Humidity
- Wind speed
- Weather conditions
- AQI level
- PM2.5
- PM10
- NO₂
- O₃
- CO

---

## 🧠 Environmental Intelligence

The platform combines:

- Satellite evidence
- Live pollutant information
- Weather conditions
- Regional administrative boundaries
- Fire-detection evidence

It produces evidence levels and environmental concern summaries.

AstraAir reports possible environmental influence and does not claim definite source causation without ground validation.

---

## 🤖 Machine-Learning Roadmap

AstraAir is building an automated environmental training dataset containing:

- HCHO
- Aerosol Index
- Fire evidence
- Surface pollutants
- Weather conditions
- AQI target levels

The current dataset is being collected and validated before model training.

Future ML development will include:

- Baseline models
- Random Forest
- Gradient Boosting
- Model comparison
- Feature importance
- Explainable AI
- Prediction confidence

---

## ✨ Current Features

- Live Weather Dashboard
- Live AQI Monitoring
- Interactive India AQI Map
- Environmental Analytics
- Live AI Insights
- PDF Environmental Reports
- Satellite Intelligence Dashboard
- Regional Satellite Evidence Engine
- Satellite + AQI + Weather Fusion
- Training Data Monitoring Dashboard

---

## 🛠️ Technology Stack

- Python
- Streamlit
- Pandas
- Plotly
- Folium
- Google Earth Engine
- Sentinel-5P
- NASA FIRMS
- OpenWeather API
- FPDF
- Git and GitHub

---

## 🏗️ Platform Architecture

```text
Satellite Observations
    ↓
Google Earth Engine Processing
    ↓
Regional Satellite Statistics
    ↓
Live AQI + Pollutants + Weather
    ↓
Environmental Fusion Engine
    ↓
Analytics + Insights + Reports
    ↓
Machine-Learning Dataset Pipeline

---

## 👨‍💻 Developer

**Dinesh Singh**

B.Tech Student

Project:
**AstraAir — AI Powered Environmental Intelligence Platform**

Version: **2.0**
""")