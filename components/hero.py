import streamlit as st

def hero():

    st.markdown("""
    <div style="
    padding:40px;
    border-radius:20px;
    background:linear-gradient(90deg,#1565C0,#29B6F6);
    text-align:center;
    color:white;
    ">
    <h1>🌍 AstraAir</h1>
    <h3>AI Powered Environmental Intelligence Platform</h3>
    <p>From Space to Smarter Air</p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Cities", "500+")
    c2.metric("Satellite", "Live")
    c3.metric("AI Accuracy", "96%")
    c4.metric("Forecast", "24 Hours")