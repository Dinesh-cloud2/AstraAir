import streamlit as st

def features():

    st.subheader("🚀 Platform Features")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.info("""
🛰️ **Satellite Intelligence**

• Sentinel-5P

• MODIS

• Google Earth Engine
""")

    with col2:
        st.success("""
🤖 **AI Prediction**

• Random Forest

• XGBoost

• Explainable AI
""")

    with col3:
        st.warning("""
🌍 **Live Monitoring**

• AQI

• Weather

• Forecast
""")