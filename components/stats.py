import streamlit as st

def stats():

    c1,c2,c3,c4=st.columns(4)

    c1.metric("Cities","500+")
    c2.metric("Satellite","Live")
    c3.metric("Model Accuracy","96%")
    c4.metric("Prediction","24 Hours")