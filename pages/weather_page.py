import streamlit as st

from services.weather import get_weather


def weather_page():

    st.title("🌦️ Live Weather Dashboard")

    st.caption(
        "Live weather data from OpenWeather — "
        "automatically refreshed every 10 minutes."
    )

    # Previous weather result ko save rakhna
    if "weather_result" not in st.session_state:
        st.session_state.weather_result = None

    if "weather_city" not in st.session_state:
        st.session_state.weather_city = "Delhi"

    city = st.text_input(
        "Enter City",
        value=st.session_state.weather_city
    )

    search_col, refresh_col = st.columns(2)

    with search_col:
        search_clicked = st.button(
            "🔍 Get Weather",
            type="primary",
            use_container_width=True
        )

    with refresh_col:
        refresh_clicked = st.button(
            "🔄 Refresh Live Data",
            use_container_width=True
        )

    # Normal city search
    if search_clicked:

        city = city.strip()

        if not city:
            st.warning("Please enter a city name.")

        else:
            with st.spinner(
                f"Loading live weather for {city}..."
            ):
                weather = get_weather(city)

            st.session_state.weather_result = weather
            st.session_state.weather_city = city

    # Cache clear karke same city ka fresh data
    if refresh_clicked:

        get_weather.clear()

        current_city = city.strip()

        if not current_city:
            current_city = st.session_state.weather_city

        with st.spinner(
            f"Refreshing live weather for {current_city}..."
        ):
            weather = get_weather(current_city)

        st.session_state.weather_result = weather
        st.session_state.weather_city = current_city

    # Saved result display
    weather = st.session_state.weather_result
    saved_city = st.session_state.weather_city

    if weather:

        st.success(
            f"Live weather for {saved_city}"
        )

        c1, c2, c3, c4 = st.columns(4)

        c1.metric(
            "🌡️ Temperature",
            f"{weather['temperature']} °C"
        )

        c2.metric(
            "💧 Humidity",
            f"{weather['humidity']} %"
        )

        c3.metric(
            "🌬️ Wind Speed",
            f"{weather['wind']} m/s"
        )

        c4.metric(
            "☁️ Condition",
            weather["description"]
        )

        icon_url = (
            "https://openweathermap.org/img/wn/"
            f"{weather['icon']}@2x.png"
        )

        st.image(
            icon_url,
            width=100
        )

        st.info(
            "Use **Refresh Live Data** to immediately request "
            "new data instead of waiting for the 10-minute cache."
        )

    elif search_clicked or refresh_clicked:

        st.error(
            "Weather data could not be loaded. "
            "Check the city name, API key, or internet connection."
        )

    else:

        st.info(
            "Enter a city and click **Get Weather**."
        )