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