import streamlit as st

def stats():

    st.markdown("## 📊 Live Platform Statistics")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("🌍 Cities", "500+")
    c2.metric("🛰️ Satellites", "3")
    c3.metric("🤖 AI Accuracy", "96%")
    c4.metric("📈 Forecast", "24 Hours")