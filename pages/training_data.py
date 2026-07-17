from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


DATA_FILE = Path(
    "data/training/environmental_training_data.csv"
)


FEATURE_COLUMNS = [
    "hcho_mean",
    "aerosol_mean",
    "fire_detection_pixels",
    "surface_no2",
    "pm2_5",
    "pm10",
    "temperature",
    "humidity",
    "wind",
    "target_aqi_level",
]


AQI_LEVEL_NAMES = {
    1: "Good",
    2: "Fair",
    3: "Moderate",
    4: "Poor",
    5: "Very Poor",
}


FEATURE_DESCRIPTIONS = {
    "hcho_mean": (
        "Mean Sentinel-5P formaldehyde column density "
        "for the selected region."
    ),
    "aerosol_mean": (
        "Mean Sentinel-5P absorbing aerosol index."
    ),
    "fire_detection_pixels": (
        "Number of FIRMS thermal-anomaly detection pixels. "
        "This is not the same as confirmed individual fires."
    ),
    "surface_no2": (
        "Average surface-level nitrogen dioxide observation."
    ),
    "pm2_5": (
        "Fine particulate matter concentration."
    ),
    "pm10": (
        "Coarse particulate matter concentration."
    ),
    "temperature": (
        "Average surface air temperature in degrees Celsius."
    ),
    "humidity": (
        "Average relative humidity percentage."
    ),
    "wind": (
        "Average wind speed in metres per second."
    ),
    "target_aqi_level": (
        "OpenWeather AQI category from 1 Good to 5 Very Poor. "
        "This is the current prototype ML target."
    ),
}


def training_data_page():

    st.title("🧠 AstraAir Training Data Center")

    st.write(
        "Monitor the environmental dataset being collected "
        "for future machine-learning experiments."
    )

    st.caption(
        "New cities and regions automatically appear here "
        "after the AstraAir data collector saves their records."
    )

    st.divider()

    # ==========================================
    # CHECK DATASET
    # ==========================================

    if not DATA_FILE.exists():

        st.error(
            "Training dataset not found at: "
            "`data/training/environmental_training_data.csv`"
        )

        st.info(
            "Run the training-data collector before opening "
            "this dashboard."
        )

        return

    try:

        df = pd.read_csv(DATA_FILE)

    except Exception as error:

        st.error(
            "Unable to read the training dataset."
        )

        st.code(str(error))

        return

    if df.empty:

        st.warning(
            "The training dataset is currently empty."
        )

        return

    # ==========================================
    # REQUIRED COLUMN CHECK
    # ==========================================

    required_columns = [
        "collected_at_utc",
        "region",
    ]

    missing_required_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_required_columns:

        st.error(
            "Required columns are missing: "
            + ", ".join(missing_required_columns)
        )

        return

    # ==========================================
    # CLEAN DATA
    # ==========================================

    df["collected_at_utc"] = pd.to_datetime(
        df["collected_at_utc"],
        utc=True,
        errors="coerce",
    )

    df["region"] = (
        df["region"]
        .astype(str)
        .str.strip()
    )

    available_features = [
        column
        for column in FEATURE_COLUMNS
        if column in df.columns
    ]

    for column in available_features:

        df[column] = pd.to_numeric(
            df[column],
            errors="coerce",
        )

    duplicate_count = int(
        df.duplicated().sum()
    )

    clean_df = (
        df.drop_duplicates()
        .copy()
    )

    if "target_aqi_level" in clean_df.columns:

        clean_df["aqi_category"] = (
            clean_df["target_aqi_level"]
            .round()
            .map(AQI_LEVEL_NAMES)
            .fillna("Unknown")
        )

    # ==========================================
    # SIDEBAR FILTERS
    # ==========================================

    st.sidebar.header(
        "🧠 Training Data Filters"
    )

    regions = sorted(
        clean_df["region"]
        .dropna()
        .unique()
        .tolist()
    )

    selected_regions = st.sidebar.multiselect(
        "Select Cities / Regions",
        options=regions,
        default=regions,
    )

    if selected_regions:

        filtered_df = clean_df[
            clean_df["region"].isin(
                selected_regions
            )
        ].copy()

    else:

        filtered_df = clean_df.copy()

    if filtered_df.empty:

        st.warning(
            "No records match the selected filters."
        )

        return

    # ==========================================
    # CORE METRICS
    # ==========================================

    total_samples = len(filtered_df)

    total_regions = int(
        filtered_df["region"].nunique()
    )

    missing_values = int(
        filtered_df.isnull()
        .sum()
        .sum()
    )

    latest_collection = (
        filtered_df["collected_at_utc"]
        .max()
    )

    unique_collection_days = int(
        filtered_df["collected_at_utc"]
        .dropna()
        .dt.date
        .nunique()
    )

    total_features = len(
        available_features
    )

    satellite_features = len(
        [
            feature
            for feature in [
                "hcho_mean",
                "aerosol_mean",
                "fire_detection_pixels",
                "surface_no2",
            ]
            if feature in available_features
        ]
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "📊 Total Samples",
        total_samples,
    )

    c2.metric(
        "🌍 Cities / Regions",
        total_regions,
    )

    c3.metric(
        "🧪 ML Features",
        total_features,
    )

    c4.metric(
        "🛰 Satellite Features",
        satellite_features,
    )

    c5, c6, c7, c8 = st.columns(4)

    c5.metric(
        "📅 Collection Days",
        unique_collection_days,
    )

    c6.metric(
        "⚠️ Missing Values",
        missing_values,
    )

    c7.metric(
        "📑 Duplicate Rows",
        duplicate_count,
    )

    if pd.notna(latest_collection):

        latest_text = (
            latest_collection
            .strftime("%d %b %Y")
        )

    else:

        latest_text = "Unknown"

    c8.metric(
        "🕒 Latest Collection",
        latest_text,
    )

    st.divider()

    # ==========================================
    # ML READINESS
    # ==========================================

    st.subheader(
        "🤖 ML Dataset Readiness"
    )

    sample_score = min(
        total_samples / 500,
        1.0,
    )

    region_score = min(
        total_regions / 20,
        1.0,
    )

    date_score = min(
        unique_collection_days / 30,
        1.0,
    )

    quality_score = (
        1.0
        if missing_values == 0
        else max(
            0.0,
            1.0 - (
                missing_values
                / max(filtered_df.size, 1)
            )
        )
    )

    readiness_score = (
        sample_score * 0.40
        + region_score * 0.25
        + date_score * 0.20
        + quality_score * 0.15
    )

    readiness_percentage = round(
        readiness_score * 100
    )

    st.progress(
        float(readiness_score)
    )

    st.write(
        f"Dataset readiness score: "
        f"**{readiness_percentage}%**"
    )

    check1, check2 = st.columns(2)

    with check1:

        if total_samples >= 100:

            st.success(
                "✅ Prototype sample milestone reached"
            )

        else:

            st.warning(
                f"⚠️ {100 - total_samples} more samples "
                "needed for the first prototype milestone"
            )

        if total_regions >= 10:

            st.success(
                "✅ Good regional coverage"
            )

        else:

            st.warning(
                "⚠️ Add more cities and regions"
            )

    with check2:

        if unique_collection_days >= 30:

            st.success(
                "✅ Good collection-day coverage"
            )

        else:

            st.warning(
                "⚠️ More time-separated collection days needed"
            )

        if (
            missing_values == 0
            and duplicate_count == 0
        ):

            st.success(
                "✅ No missing or duplicate records detected"
            )

        else:

            st.warning(
                "⚠️ Dataset quality issues require review"
            )

    if total_samples < 100:

        st.warning(
            "The dataset is not ready for reliable ML training. "
            "Continue collecting time-separated observations."
        )

    elif total_samples < 500:

        st.info(
            "Initial experimental ML testing can begin, "
            "but more historical samples are recommended."
        )

    else:

        st.success(
            "The dataset has reached the larger "
            "experimental milestone."
        )

    st.caption(
        "This readiness score is a project-development metric. "
        "It is not proof of scientific or production readiness."
    )

    st.divider()

    # ==========================================
    # CITY / REGION COVERAGE
    # ==========================================

    st.subheader(
        "🌍 Samples by City / Region"
    )

    region_counts = (
        filtered_df["region"]
        .value_counts()
        .reset_index()
    )

    region_counts.columns = [
        "City / Region",
        "Samples",
    ]

    region_fig = px.bar(
        region_counts,
        x="City / Region",
        y="Samples",
        color="Samples",
        title="Training Samples by City / Region",
    )

    region_fig.update_layout(
        xaxis_tickangle=-45
    )

    st.plotly_chart(
        region_fig,
        use_container_width=True,
    )

    st.info(
        "To increase city or regional coverage, update the "
        "training-data collector. This dashboard will then "
        "display the new locations automatically."
    )

    st.divider()

    # ==========================================
    # COLLECTION TIMELINE
    # ==========================================

    st.subheader(
        "📅 Dataset Collection Timeline"
    )

    timeline_df = (
        filtered_df
        .dropna(
            subset=["collected_at_utc"]
        )
        .copy()
    )

    if not timeline_df.empty:

        timeline_df["Collection Date"] = (
            timeline_df["collected_at_utc"]
            .dt.date
        )

        timeline_counts = (
            timeline_df
            .groupby("Collection Date")
            .size()
            .reset_index(
                name="Samples"
            )
        )

        timeline_counts[
            "Cumulative Samples"
        ] = timeline_counts[
            "Samples"
        ].cumsum()

        timeline_fig = px.line(
            timeline_counts,
            x="Collection Date",
            y="Cumulative Samples",
            markers=True,
            title="Environmental Dataset Growth",
        )

        st.plotly_chart(
            timeline_fig,
            use_container_width=True,
        )

    else:

        st.info(
            "Collection timeline is unavailable."
        )

    st.divider()

    # ==========================================
    # AQI TARGET DISTRIBUTION
    # ==========================================

    if "target_aqi_level" in filtered_df.columns:

        st.subheader(
            "🌫 AQI Target Distribution"
        )

        aqi_counts = (
            filtered_df["target_aqi_level"]
            .round()
            .value_counts()
            .sort_index()
            .reset_index()
        )

        aqi_counts.columns = [
            "AQI Level",
            "Samples",
        ]

        aqi_counts["Category"] = (
            aqi_counts["AQI Level"]
            .map(AQI_LEVEL_NAMES)
            .fillna("Unknown")
        )

        aqi_fig = px.bar(
            aqi_counts,
            x="Category",
            y="Samples",
            color="AQI Level",
            title="Training Samples by AQI Target Category",
        )

        st.plotly_chart(
            aqi_fig,
            use_container_width=True,
        )

        st.caption(
            "The current target is the OpenWeather AQI category "
            "from 1 Good to 5 Very Poor."
        )

        st.divider()

    # ==========================================
    # FEATURE DESCRIPTIONS
    # ==========================================

    st.subheader(
        "📘 Environmental Feature Guide"
    )

    feature_description_rows = []

    for feature in available_features:

        feature_description_rows.append(
            {
                "Feature": feature,
                "Description": FEATURE_DESCRIPTIONS.get(
                    feature,
                    "Environmental training feature.",
                ),
            }
        )

    st.dataframe(
        pd.DataFrame(
            feature_description_rows
        ),
        use_container_width=True,
        hide_index=True,
    )

    st.divider()

    # ==========================================
    # FEATURE STATISTICS
    # ==========================================

    st.subheader(
        "📊 Environmental Feature Statistics"
    )

    if available_features:

        statistics = (
            filtered_df[available_features]
            .describe()
            .round(5)
            .T
        )

        st.dataframe(
            statistics,
            use_container_width=True,
        )

    else:

        st.warning(
            "No environmental feature columns "
            "were found."
        )

        return

    st.divider()

    # ==========================================
    # FEATURE DISTRIBUTION
    # ==========================================

    st.subheader(
        "🔬 Feature Distribution Explorer"
    )

    selected_feature = st.selectbox(
        "Select Environmental Feature",
        available_features,
    )

    feature_fig = px.histogram(
        filtered_df,
        x=selected_feature,
        color="region",
        nbins=30,
        title=(
            f"{selected_feature} Distribution"
        ),
    )

    st.plotly_chart(
        feature_fig,
        use_container_width=True,
    )

    selected_description = (
        FEATURE_DESCRIPTIONS.get(
            selected_feature,
            "Environmental training feature.",
        )
    )

    st.info(
        f"**{selected_feature}:** "
        f"{selected_description}"
    )

    st.divider()

    # ==========================================
    # FEATURE COMPARISON
    # ==========================================

    st.subheader(
        "📈 Feature Comparison"
    )

    comparison_feature = st.selectbox(
        "Select Feature for Regional Comparison",
        available_features,
        key="comparison_feature",
    )

    comparison_df = (
        filtered_df
        .groupby("region")[
            comparison_feature
        ]
        .mean()
        .reset_index()
    )

    comparison_df.columns = [
        "City / Region",
        f"Average {comparison_feature}",
    ]

    comparison_fig = px.bar(
        comparison_df,
        x="City / Region",
        y=f"Average {comparison_feature}",
        color=f"Average {comparison_feature}",
        title=(
            f"Average {comparison_feature} "
            "by City / Region"
        ),
    )

    comparison_fig.update_layout(
        xaxis_tickangle=-45
    )

    st.plotly_chart(
        comparison_fig,
        use_container_width=True,
    )

    st.divider()

    # ==========================================
    # CORRELATION MATRIX
    # ==========================================

    if len(available_features) >= 2:

        st.subheader(
            "🔗 Environmental Feature Correlation"
        )

        correlation_df = (
            filtered_df[available_features]
            .corr()
            .round(2)
        )

        correlation_fig = px.imshow(
            correlation_df,
            text_auto=True,
            aspect="auto",
            title="Feature Correlation Matrix",
        )

        st.plotly_chart(
            correlation_fig,
            use_container_width=True,
        )

        st.caption(
            "Correlation indicates association between "
            "features. It does not prove causation."
        )

        st.divider()

    # ==========================================
    # DATA QUALITY
    # ==========================================

    st.subheader(
        "🔎 Data Quality"
    )

    missing_df = (
        filtered_df
        .isnull()
        .sum()
        .reset_index()
    )

    missing_df.columns = [
        "Feature",
        "Missing Values",
    ]

    missing_df = missing_df[
        missing_df["Missing Values"] > 0
    ]

    filtered_duplicate_count = int(
        filtered_df.duplicated().sum()
    )

    completeness = round(
        (
            1
            - missing_values
            / max(
                filtered_df.size,
                1,
            )
        )
        * 100,
        2,
    )

    q1, q2, q3 = st.columns(3)

    q1.metric(
        "Missing Cells",
        missing_values,
    )

    q2.metric(
        "Duplicate Rows",
        filtered_duplicate_count,
    )

    q3.metric(
        "Data Completeness",
        f"{completeness}%",
    )

    if (
        missing_df.empty
        and filtered_duplicate_count == 0
    ):

        st.success(
            "No missing values or duplicate rows detected."
        )

    else:

        if not missing_df.empty:

            st.warning(
                "Missing values were detected."
            )

            st.dataframe(
                missing_df,
                use_container_width=True,
                hide_index=True,
            )

        if filtered_duplicate_count > 0:

            st.warning(
                f"{filtered_duplicate_count} duplicate rows "
                "were detected."
            )

    st.divider()

    # ==========================================
    # RAW DATA AND DOWNLOAD
    # ==========================================

    with st.expander(
        "📂 View Training Dataset"
    ):

        st.dataframe(
            filtered_df,
            use_container_width=True,
            hide_index=True,
        )

        st.download_button(
            "📥 Download Filtered Training Dataset",
            data=filtered_df.to_csv(
                index=False
            ),
            file_name=(
                "astraair_environmental_training_data.csv"
            ),
            mime="text/csv",
            use_container_width=True,
        )

    st.divider()

    st.info(
        "AstraAir's training dataset combines satellite "
        "observations, weather variables, surface-pollution "
        "measurements and AQI target categories. The dataset "
        "is still being expanded before reliable machine-"
        "learning model training begins."
    )