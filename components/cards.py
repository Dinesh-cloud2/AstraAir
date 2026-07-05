
import streamlit as st

def cards():

    c1,c2,c3,c4=st.columns(4)

    c1.metric("🌍 Cities","500+")

    c2.metric("🛰 Satellites","Live")

    c3.metric("🤖 AI Models","4")

    c4.metric("⚡ Status","Online")