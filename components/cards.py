import streamlit as st

def cards():

    c1, c2, c3 = st.columns(3)

    with c1:
        st.info("🛰️ Satellite Data")
        st.write("Real-time environmental monitoring from space.")

    with c2:
        st.success("🌦️ Weather Intelligence")
        st.write("Live weather updates and forecasting.")

    with c3:
        st.warning("🤖 AI Insights")
        st.write("AI-powered air quality analysis and predictions.")