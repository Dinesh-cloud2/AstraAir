import streamlit as st


def hero():

    hero_html = """
    <section class="astra-hero">

        <div class="astra-hero-ambient astra-hero-ambient-one"></div>
        <div class="astra-hero-ambient astra-hero-ambient-two"></div>

        <div class="astra-hero-content">

            <div class="astra-hero-badge">
                <span class="astra-hero-badge-dot"></span>
                Satellite-Powered Environmental Intelligence
            </div>

            <h1 class="astra-hero-title">
                From Space to
                <span>Smarter Air</span>
            </h1>

            <p class="astra-hero-description">
                Explore current air-quality observations, pollutant
                patterns, weather conditions, satellite evidence and
                transparent environmental insights across India.
            </p>

            <div class="astra-hero-actions">

                <a
                    href="?page=aqi-map"
                    target="_self"
                    class="astra-hero-button astra-hero-button-primary"
                >
                    Explore Live AQI
                    <span>→</span>
                </a>

                <a
                    href="?page=satellite"
                    target="_self"
                    class="astra-hero-button astra-hero-button-secondary"
                >
                    View Satellite Data
                </a>

            </div>

            <div class="astra-hero-tags">

                <div class="astra-hero-tag">
                    <strong>60+</strong>
                    <span>Cities Covered</span>
                </div>

                <div class="astra-hero-tag">
                    <strong>4</strong>
                    <span>Satellite Layers</span>
                </div>

                <div class="astra-hero-tag">
                    <strong>Live</strong>
                    <span>AQI &amp; Weather</span>
                </div>

                <div class="astra-hero-tag">
                    <strong>V3</strong>
                    <span>AstraAir Platform</span>
                </div>

            </div>

        </div>

        <div class="astra-hero-visual">

            <div class="astra-visual-glow"></div>

            <div class="astra-orbit astra-orbit-one"></div>
            <div class="astra-orbit astra-orbit-two"></div>
            <div class="astra-orbit astra-orbit-three"></div>

            <div class="astra-earth">
                <div class="astra-earth-light"></div>
                <div class="astra-earth-icon">🌍</div>
            </div>

            <div class="astra-satellite-icon">🛰️</div>

            <div class="astra-visual-status">

                <span class="astra-visual-status-dot"></span>

                <div>
                    <strong>Live Systems</strong>
                    <span>Environmental feeds connected</span>
                </div>

            </div>

        </div>

    </section>
    """

    st.html(hero_html)