import streamlit as st


def cards():

    section_html = """
    <section class="astra-capabilities-section">

        <div class="astra-section-heading">

            <div>
                <span class="astra-section-kicker">
                    Platform Capabilities
                </span>

                <h2>
                    Environmental intelligence,
                    built for real-world understanding
                </h2>
            </div>

            <p>
                AstraAir combines live environmental data,
                satellite observations, analytics and transparent
                insights in one unified platform.
            </p>

        </div>

        <div class="astra-feature-grid">

            <a
                class="astra-feature-card"
                href="?page=satellite"
                target="_self"
            >

                <div class="astra-feature-card-top">

                    <div class="astra-feature-icon">
                        🛰️
                    </div>

                    <div class="astra-feature-arrow">
                        ↗
                    </div>

                </div>

                <h3>Satellite Intelligence</h3>

                <p>
                    Analyze Sentinel-5P and NASA FIRMS observations
                    to understand aerosol activity, fire detections
                    and atmospheric pollution patterns.
                </p>

                <span class="astra-feature-link">
                    Explore satellite data
                    <span>→</span>
                </span>

            </a>


            <a
                class="astra-feature-card"
                href="?page=weather"
                target="_self"
            >

                <div class="astra-feature-card-top">

                    <div class="astra-feature-icon">
                        🌦️
                    </div>

                    <div class="astra-feature-arrow">
                        ↗
                    </div>

                </div>

                <h3>Live Environmental Monitoring</h3>

                <p>
                    Monitor live AQI, PM2.5, PM10, temperature,
                    humidity and weather conditions across Indian
                    cities.
                </p>

                <span class="astra-feature-link">
                    View live conditions
                    <span>→</span>
                </span>

            </a>


            <a
                class="astra-feature-card"
                href="?page=insights"
                target="_self"
            >

                <div class="astra-feature-card-top">

                    <div class="astra-feature-icon">
                        🤖
                    </div>

                    <div class="astra-feature-arrow">
                        ↗
                    </div>

                </div>

                <h3>Environmental Intelligence</h3>

                <p>
                    Combine satellite evidence, weather information
                    and pollutant measurements to generate clear,
                    explainable environmental insights.
                </p>

                <span class="astra-feature-link">
                    Generate insights
                    <span>→</span>
                </span>

            </a>


            <a
                class="astra-feature-card"
                href="?page=analytics"
                target="_self"
            >

                <div class="astra-feature-card-top">

                    <div class="astra-feature-icon">
                        📊
                    </div>

                    <div class="astra-feature-arrow">
                        ↗
                    </div>

                </div>

                <h3>Interactive Analytics</h3>

                <p>
                    Visualize pollutant trends, compare cities and
                    explore environmental indicators through
                    interactive dashboards.
                </p>

                <span class="astra-feature-link">
                    Open analytics
                    <span>→</span>
                </span>

            </a>


            <a
                class="astra-feature-card"
                href="?page=reports"
                target="_self"
            >

                <div class="astra-feature-card-top">

                    <div class="astra-feature-icon">
                        📄
                    </div>

                    <div class="astra-feature-arrow">
                        ↗
                    </div>

                </div>

                <h3>Smart Environmental Reports</h3>

                <p>
                    Generate downloadable reports containing current
                    AQI, pollutants, weather observations and health
                    recommendations.
                </p>

                <span class="astra-feature-link">
                    Create a report
                    <span>→</span>
                </span>

            </a>


            <a
                class="astra-feature-card"
                href="?page=training"
                target="_self"
            >

                <div class="astra-feature-card-top">

                    <div class="astra-feature-icon">
                        🧠
                    </div>

                    <div class="astra-feature-arrow">
                        ↗
                    </div>

                </div>

                <h3>Machine Learning Ready</h3>

                <p>
                    Build and monitor an automated environmental
                    training dataset designed for future prediction
                    models and Explainable AI.
                </p>

                <span class="astra-feature-link">
                    View training data
                    <span>→</span>
                </span>

            </a>

        </div>

    </section>
    """

    st.html(section_html)