import streamlit as st

def sidebar():
    with st.sidebar:
        st.title("🛰️ AstraAir")
        st.caption("From Space to Smarter Air")

        st.divider()

        page = st.radio(
            "Navigation",
            [
                "🏠 Home",
                "🌦️ Weather",
                "🗺️ AQI Map",
                "📊 Analytics",
                "🤖 AI Insights",
                "📄 Reports",
                "ℹ️ About"
            ]
        )

        st.divider()
        st.success("🟢 System Online")

    return page