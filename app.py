import streamlit as st

from components.sidebar import sidebar
from pages.map_page import map_page
from components.navbar import navbar
from components.hero import hero
from components.cards import cards
from pages.analytics import analytics_page
from components.stats import stats
from pages.weather_page import weather_page
from components.footer import footer
from pages.reports import reports_page
from pages.ai_insights import ai_insights_page
from pages.about import about_page
from pages.satellite_page import satellite_page
from pages.satellite_dashboard import satellite_dashboard

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

elif page == "🗺️ AQI Map":
    map_page()
    footer()
elif page == "📊 Analytics":
    analytics_page()
    footer()
elif page == "🤖 AI Insights":
    ai_insights_page()
    footer()
elif page == "📄 Reports":
    reports_page()
    footer()
elif page == "ℹ️ About":
    about_page()
    footer()
elif page == "🛰️ Satellite Explorer":
    satellite_page()
    footer()
elif page == "🛰️ Satellite Intelligence":
    satellite_dashboard()
    footer()
else:
    st.title(page)
    st.info("This page will be built in the next sprint.")
    footer()