import streamlit as st


def about_page():

    st.title("🛰️ About AstraAir")

    st.caption(
        "Satellite-powered environmental intelligence "
        "for clearer air-quality understanding."
    )

    # ==========================================
    # HERO SECTION
    # ==========================================

    st.markdown(
        """
## AstraAir

### **From Space to Smarter Air**

AstraAir is an environmental intelligence platform that
combines satellite observations, current air-pollution data,
weather conditions, analytics, reports, and transparent
environmental interpretation.

The project aims to make complex environmental information
easier to explore and understand.
"""
    )

    st.divider()

    # ==========================================
    # PROJECT OVERVIEW
    # ==========================================

    st.subheader("🎯 Project Vision")

    st.write(
        "AstraAir is designed to connect satellite-based "
        "environmental observations with current surface-level "
        "air-quality and weather information."
    )

    st.write(
        "The platform helps users explore questions such as:"
    )

    st.markdown(
        """
- What is the current air-quality category?
- Which pollutants are elevated?
- What do recent satellite observations show?
- Are aerosol, formaldehyde, nitrogen-dioxide, or fire signals present?
- How might weather conditions influence pollutant dispersion?
- What general health precautions may be appropriate?
"""
    )

    st.divider()

    # ==========================================
    # PROBLEM STATEMENT
    # ==========================================

    st.subheader("🌫️ Problem Statement")

    st.write(
        "Air-pollution information is often distributed across "
        "different platforms and presented using technical formats "
        "that are difficult for ordinary users to interpret."
    )

    st.write(
        "Ground observations provide useful local measurements, "
        "while satellite datasets offer broader regional coverage. "
        "AstraAir brings these sources together in one interactive "
        "platform."
    )

    st.divider()

    # ==========================================
    # KEY CAPABILITIES
    # ==========================================

    st.subheader("✨ Current Platform Capabilities")

    feature_col1, feature_col2 = st.columns(2)

    with feature_col1:

        st.markdown(
            """
#### 🌍 Live Environmental Monitoring

- Current OpenWeather AQI category
- PM2.5 and PM10 observations
- NO₂, O₃, and CO observations
- Temperature, humidity, and wind
- Multi-city weather coverage
- State-filtered AQI map
"""
        )

        st.markdown(
            """
#### 📊 Analytics and Reports

- State-filtered pollution analytics
- Pollutant comparison charts
- Highest and lowest pollution observations
- Explainable rule-based insights
- Downloadable PDF environmental reports
"""
        )

    with feature_col2:

        st.markdown(
            """
#### 🛰️ Satellite Intelligence

- Sentinel-5P NO₂
- Sentinel-5P HCHO / Formaldehyde
- Sentinel-5P Absorbing Aerosol Index
- NASA FIRMS thermal-anomaly observations
- Regional satellite-layer exploration
- Administrative-boundary analysis
"""
        )

        st.markdown(
            """
#### 🧠 Data and Intelligence

- Regional Satellite Evidence Engine
- Satellite + current environmental fusion
- Automated training-data collection
- Dataset-quality validation
- Machine-learning readiness monitoring
"""
        )

    st.divider()

    # ==========================================
    # SATELLITE SECTION
    # ==========================================

    st.subheader("🛰️ Satellite Intelligence")

    st.write(
        "AstraAir uses Google Earth Engine to process and display "
        "environmental satellite observations."
    )

    satellite_data = {
        "Dataset": [
            "Sentinel-5P NO₂",
            "Sentinel-5P HCHO",
            "Sentinel-5P Aerosol Index",
            "NASA FIRMS",
        ],
        "Purpose": [
            "Regional nitrogen-dioxide observation",
            "Formaldehyde and VOC-related atmospheric signal",
            "Detection of UV-absorbing aerosol plumes",
            "Active-fire and thermal-anomaly evidence",
        ],
    }

    st.dataframe(
        satellite_data,
        use_container_width=True,
        hide_index=True,
    )

    st.info(
        "Satellite observations provide regional atmospheric "
        "evidence. They are not the same as ground-level pollutant "
        "concentrations measured by monitoring stations."
    )

    st.divider()

    # ==========================================
    # LIVE DATA SECTION
    # ==========================================

    st.subheader("🌍 Current Environmental Data")

    st.write(
        "AstraAir uses the OpenWeather APIs to retrieve current "
        "weather and air-pollution observations using city "
        "coordinates."
    )

    live_col1, live_col2, live_col3 = st.columns(3)

    with live_col1:
        st.markdown(
            """
#### Air Quality

- AQI category: 1–5
- PM2.5
- PM10
"""
        )

    with live_col2:
        st.markdown(
            """
#### Gaseous Pollutants

- NO₂
- O₃
- CO
"""
        )

    with live_col3:
        st.markdown(
            """
#### Weather

- Temperature
- Humidity
- Wind speed
- Weather condition
"""
        )

    st.caption(
        "Current API observations may differ from official CPCB "
        "monitoring-station measurements."
    )

    st.divider()

    # ==========================================
    # ENVIRONMENTAL INTELLIGENCE
    # ==========================================

    st.subheader("🧠 Environmental Intelligence")

    st.write(
        "AstraAir combines multiple signals to produce transparent "
        "environmental summaries."
    )

    st.markdown(
        """
The current interpretation system considers:

- Satellite HCHO observations
- Absorbing Aerosol Index
- FIRMS thermal-anomaly evidence
- Current particulate-matter observations
- Current gaseous-pollutant observations
- Wind speed
- Humidity
- Temperature
"""
    )

    st.warning(
        "The current intelligence engine is rule-based. "
        "It does not prove pollution-source causation and should "
        "not be presented as a trained machine-learning prediction."
    )

    st.divider()

    # ==========================================
    # TRAINING DATA
    # ==========================================

    st.subheader("🤖 Machine-Learning Dataset Development")

    st.write(
        "AstraAir is collecting a city-level environmental dataset "
        "for future machine-learning experiments."
    )

    st.markdown(
        """
The training pipeline currently stores:

- City, state, latitude, and longitude
- Collection timestamp
- Satellite HCHO
- Satellite Aerosol Index
- Fire-detection pixels
- Surface NO₂
- PM2.5 and PM10
- O₃ and CO
- Temperature
- Humidity
- Wind speed
- OpenWeather AQI target category
"""
    )

    st.info(
        "Model training will begin only after sufficient "
        "time-separated observations and regional coverage "
        "have been collected."
    )

    st.divider()

    # ==========================================
    # ARCHITECTURE
    # ==========================================

    st.subheader("🏗️ Platform Architecture")

    st.code(
        """
Satellite Observations
        ↓
Google Earth Engine Processing
        ↓
Regional Satellite Statistics
        ↓
Current AQI + Pollutants + Weather
        ↓
Environmental Evidence and Fusion
        ↓
Maps + Analytics + Insights + Reports
        ↓
Environmental Training Dataset
        ↓
Future ML Model + Explainability
""",
        language="text",
    )

    st.divider()

    # ==========================================
    # TECHNOLOGY STACK
    # ==========================================

    st.subheader("🛠️ Technology Stack")

    stack_col1, stack_col2, stack_col3 = st.columns(3)

    with stack_col1:
        st.markdown(
            """
#### Application

- Python
- Streamlit
- Pandas
- Requests
"""
        )

    with stack_col2:
        st.markdown(
            """
#### Visualization

- Plotly
- Folium
- Streamlit-Folium
- FPDF2
"""
        )

    with stack_col3:
        st.markdown(
            """
#### Environmental Sources

- Google Earth Engine
- Sentinel-5P
- NASA FIRMS
- OpenWeather API
"""
        )

    st.divider()

    # ==========================================
    # SCIENTIFIC LIMITATIONS
    # ==========================================

    st.subheader("⚠️ Scientific and Data Limitations")

    st.markdown(
        """
- OpenWeather AQI uses a 1–5 category scale.
- Current API observations are not official CPCB station readings.
- Satellite column observations are not direct surface concentrations.
- Thermal-anomaly pixels do not always represent confirmed fires.
- Satellite and current surface observations may not be time-aligned.
- Rule-based evidence levels are prototype decision rules.
- Environmental association does not prove emission-source causation.
- Health recommendations are general guidance, not medical advice.
"""
    )

    st.divider()

    # ==========================================
    # DEVELOPMENT STATUS
    # ==========================================

    st.subheader("🚀 Current Development Status")

    status_data = {
        "Module": [
            "Weather Dashboard",
            "Live AQI Map",
            "Environmental Analytics",
            "Environmental Insights",
            "PDF Reports",
            "Satellite Intelligence",
            "Training Data Center",
            "ML Prediction",
        ],
        "Status": [
            "Completed",
            "Completed",
            "Completed",
            "Completed",
            "Completed",
            "Completed",
            "In active data collection",
            "Planned after dataset growth",
        ],
    }

    st.dataframe(
        status_data,
        use_container_width=True,
        hide_index=True,
    )

    st.divider()

    # ==========================================
    # ROADMAP
    # ==========================================

    st.subheader("🔭 Future Roadmap")

    st.markdown(
        """
- Continue daily city-level environmental data collection
- Add more cities and administrative regions
- Improve historical time alignment
- Integrate official ground-monitoring sources where available
- Compare baseline and tree-based ML models
- Add feature-importance analysis
- Add SHAP-based explainability
- Add prediction confidence and uncertainty reporting
- Improve accessibility and mobile responsiveness
- Deploy the final stable AstraAir release
"""
    )

    st.divider()

    # ==========================================
    # DEVELOPER
    # ==========================================

    st.subheader("👨‍💻 Developer")

    developer_col1, developer_col2 = st.columns([1, 2])

    with developer_col1:

        st.metric(
            "Project Version",
            "AstraAir V3",
        )

        st.metric(
            "Current Stage",
            # "Final Stabilization",
        )

    with developer_col2:

        st.markdown(
            """
### **Dinesh Singh**

B.Tech Student

**Project:**  
AstraAir — Satellite-Powered Environmental Intelligence Platform

**Mission:**  
To transform satellite and environmental data into clear,
interactive, and responsible air-quality insights.
"""
        )

    st.divider()

    st.success(
        "AstraAir connects space-based observations, current "
        "environmental data, and transparent analytics to support "
        "better understanding of air-quality conditions."
    )