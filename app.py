import streamlit as st

from components.navbar import navbar
from components.hero import hero
from components.cards import cards
from components.stats import stats  
from components.banner import banner
from streamlit_folium import st_folium  
from components.features import features

st.set_page_config(
page_title="AstraAir",
page_icon="🛰",
layout="wide"
)

with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>",unsafe_allow_html=True)

navbar()

hero()

features()
st.divider()

st.subheader("🌍 Our Vision")

st.write("""
AstraAir is an AI-powered Environmental Intelligence Platform that combines:

🛰️ Satellite Data

🌦️ Weather Intelligence

🤖 Artificial Intelligence

📊 Analytics

to monitor, predict, and explain air quality across India in real time.
""")

st.write("")

cards()

st.divider()

st.header("🚀 Platform")

st.write("""

AstraAir combines

🛰 Satellite Intelligence

🌦 Weather

🤖 Machine Learning

📊 Analytics

🧠 Explainable AI

to provide next generation Environmental Intelligence.

""")

st.divider()

st.success("Sprint 2 Successfully Started 🚀")