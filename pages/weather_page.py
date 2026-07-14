import streamlit as st

from services.cities import (
    get_cities,
    get_city_details,
)
from services.weather import get_weather


def weather_page():

    st.title("🌦️ Live Weather Dashboard")

    st.caption(
        "Current weather from OpenWeather — "
        "refreshed every 10 minutes."
    )

    if "weather_result" not in st.session_state:
        st.session_state.weather_result = None

    if "weather_city" not in st.session_state:
        st.session_state.weather_city = "Delhi"

    cities_df = get_cities()

    city_options = cities_df.apply(
        lambda row: f"{row['City']}, {row['State']}",
        axis=1,
    ).tolist()

    default_option = "Delhi, Delhi"

    selected_index = (
        city_options.index(default_option)
        if default_option in city_options
        else 0
    )

    selected_option = st.selectbox(
        "📍 Select City",
        city_options,
        index=selected_index,
    )

    selected_city = selected_option.split(",")[0].strip()

    city_details = get_city_details(selected_city)

    load_col, refresh_col = st.columns(2)

    with load_col:
        load_clicked = st.button(
            "🌦️ Load Live Weather",
            type="primary",
            use_container_width=True,
        )

    with refresh_col:
        refresh_clicked = st.button(
            "🔄 Refresh Live Data",
            use_container_width=True,
        )

    if load_clicked or refresh_clicked:

        if refresh_clicked:
            get_weather.clear()

        if not city_details:
            st.error("City coordinates not found.")
            return

        with st.spinner(
            f"Loading live weather for {selected_city}..."
        ):
            weather = get_weather(
                city=selected_city,
                lat=city_details["latitude"],
                lon=city_details["longitude"],
            )

        st.session_state.weather_result = weather
        st.session_state.weather_city = selected_option

    weather = st.session_state.weather_result
    saved_city = st.session_state.weather_city

    if weather:

        st.success(
            f"📍 Live weather for {saved_city}"
        )

        c1, c2, c3, c4 = st.columns(4)

        c1.metric(
            "🌡️ Temperature",
            f"{weather['temperature']} °C",
        )

        c2.metric(
            "💧 Humidity",
            f"{weather['humidity']} %",
        )

        c3.metric(
            "🌬️ Wind Speed",
            f"{weather['wind']} m/s",
        )

        c4.metric(
            "☁️ Condition",
            weather["description"],
        )

        icon_url = (
            "https://openweathermap.org/img/wn/"
            f"{weather['icon']}@2x.png"
        )

        st.image(icon_url, width=100)

    elif load_clicked or refresh_clicked:

        st.error(
            "Weather data could not be loaded."
        )

    else:

        st.info(
            "Select a city and click "
            "**Load Live Weather**."
        )