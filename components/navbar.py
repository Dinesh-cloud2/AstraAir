import streamlit as st

def navbar():

    left,right=st.columns([8,2])

    with left:
        st.title("🛰 AstraAir")

        st.caption("AI Powered Environmental Intelligence Platform")

    with right:
        st.success("🟢 LIVE")