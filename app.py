import streamlit as st
from components import stats
from components.hero import hero
from components.navbar import navbar
from components.cards import cards
from components.stats import stats
from components.footer import footer    

st.set_page_config(
    page_title="AstraAir",
    page_icon="🛰️",
    layout="wide"
)

navbar()

hero()

st.divider()
stats()             

st.divider()
cards()

footer()