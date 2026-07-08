import streamlit as st
from services.weather import get_weather

def weather_page():
    st.title("🌦️ Live Weather Dashboard")

    city = st.text_input("Enter city", "Delhi")

    if st.button("Get Live Weather"):
        weather = get_weather(city)

        if weather:
            st.success(f"Live weather for {city}")

            c1, c2, c3, c4 = st.columns(4)

            c1.metric("🌡️ Temperature", f"{weather['temperature']} °C")
            c2.metric("💧 Humidity", f"{weather['humidity']} %")
            c3.metric("🌬️ Wind Speed", f"{weather['wind']} m/s")
            c4.metric("☁️ Condition", weather["description"])

            icon_url = f"https://openweathermap.org/img/wn/{weather['icon']}@2x.png"
            st.image(icon_url, width=100)

        else:
            st.error("Weather data not found. Check city name.")