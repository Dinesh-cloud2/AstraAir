import streamlit as st


def stats():

    st.markdown("## 📊 AstraAir Platform Overview")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            "🌍 Cities Covered",
            "60+",
        )
        st.caption(
            "Live monitoring locations"
        )

    with c2:
        st.metric(
            "🛰️ Satellite Sources",
            "4",
        )
        st.caption(
            "Sentinel-5P + NASA FIRMS"
        )

    with c3:
        st.metric(
            "🌦️ Live Services",
            "2",
        )
        st.caption(
            "AQI & Weather APIs"
        )

    with c4:
        st.metric(
            "🧠 ML Status",
            "Training",
        )
        st.caption(
            "Dataset collection in progress"
        )