import streamlit as st


def footer():

    footer_html = """
<div class="astra-footer">

    <div class="astra-footer-top">

        <div>

            <div class="astra-footer-title">
                🛰️ AstraAir
            </div>

            <div class="astra-footer-tagline">
                From Space to Smarter Air
            </div>

        </div>

        <div class="astra-footer-version">
            Version 3.0
        </div>

    </div>

    <hr>

    <div class="astra-footer-grid">

        <div>

            <h4>Platform</h4>

            <p>
            AI Powered Environmental Intelligence Platform
            combining Satellite Data, Live AQI, Weather,
            Analytics and Explainable Environmental Insights.
            </p>

        </div>

        <div>

            <h4>Technology</h4>

            <p>
            Python • Streamlit • Google Earth Engine •
            Sentinel-5P • NASA FIRMS • OpenWeather API •
            Plotly • Folium
            </p>

        </div>

        <div>

            <h4>Developer</h4>

            <p>
            Dinesh Singh<br>
            B.Tech Student
            </p>

        </div>

    </div>

    <hr>

    <div class="astra-footer-bottom">

        <span>
            © 2026 AstraAir
        </span>

        <span>
            Environmental Intelligence Platform
        </span>

    </div>

</div>
"""

    st.html(footer_html)