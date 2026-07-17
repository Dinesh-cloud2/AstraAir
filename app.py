from pathlib import Path

import streamlit as st


# This must be the first Streamlit command
st.set_page_config(
    page_title="AstraAir",
    page_icon="🛰️",
    layout="wide",
)


from components.sidebar import sidebar
from components.navbar import navbar
from components.hero import hero
from components.cards import cards
from components.stats import stats
from components.footer import footer

from pages.weather_page import weather_page
from pages.map_page import map_page
from pages.analytics import analytics_page
from pages.ai_insights import ai_insights_page
from pages.reports import reports_page
from pages.about import about_page
from pages.satellite_dashboard import satellite_dashboard
from pages.training_data import training_data_page


def load_css():
    css_file = Path("assets/style.css")

    if not css_file.exists():
        st.warning(
            "UI stylesheet was not found at "
            "`assets/style.css`."
        )
        return

    css_content = css_file.read_text(
        encoding="utf-8"
    )

    st.markdown(
        f"<style>{css_content}</style>",
        unsafe_allow_html=True,
    )


load_css()

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


elif page == "🛰️ Satellite Intelligence":
    satellite_dashboard()
    footer()


elif page == "🧠 Training Data":
    training_data_page()
    footer()


elif page == "ℹ️ About":
    about_page()
    footer()


else:
    st.title(page)
    st.info(
        "This page is currently under development."
    )
    footer()