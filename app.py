import streamlit as st

from components.sidebar import sidebar
from components.navbar import navbar
from components.hero import hero
from components.cards import cards
from components.stats import stats
from pages.weather_page import weather_page
from components.footer import footer

st.set_page_config(
    page_title="AstraAir",
    page_icon="🛰️",
    layout="wide"
)

page = sidebar()

if page == "🏠 Home":
    navbar()
    hero()
    st.divider()
    stats()
    st.divider()
    cards()
    footer()
elif page == "🌦️ Weather":
    weather_page()
    footer()
else:
    st.title(page)
    st.info("This page will be built in the next sprint.")
    footer()