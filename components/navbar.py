import streamlit as st

def navbar():
    st.markdown("""
    <div style="
    padding:15px;
    background:#0E1117;
    border-radius:10px;
    color:white;
    font-size:18px;
    ">
        🛰 AstraAir | Dashboard | Live Map | AI Insights | Reports
    </div>
    """, unsafe_allow_html=True)