import streamlit as st

from components.navbar import show_navbar
from components.footer import show_footer

st.set_page_config(
    page_title="AstraAir",
    page_icon="🛰️",
    layout="wide"
)

show_navbar()

st.markdown("# 🌍 Welcome")

st.write("""
AstraAir combines

🛰️ Satellite Data

🌦 Weather

🤖 Artificial Intelligence

📊 Analytics

to monitor and predict air quality.
""")

st.info("🚀 Version 2.0 Development Started")

show_footer()