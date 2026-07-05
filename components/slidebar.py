with st.sidebar:
    st.title("🌍 AstraAir")

    page = st.radio(
        "Navigation",
        [
            "🏠 Dashboard",
            "🗺️ Live Map",
            "📊 Analytics",
            "🤖 AI Insights",
            "🚨 Alerts",
            "📄 Reports",
            "ℹ️ About"
        ]
    )

    st.divider()
    st.success("🟢 System Online")