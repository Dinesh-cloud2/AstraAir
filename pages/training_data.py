from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


DATA_FILE = Path(
    "data/training/environmental_training_data.csv"
)


def training_data_page():

    st.title("🧠 AstraAir Training Data Center")

    st.write(
        "Monitor the environmental dataset being collected "
        "for future machine-learning experiments."
    )

    st.divider()

    if not DATA_FILE.exists():

        st.error(
            "Training dataset not found. "
            "Run the data collector first."
        )

        return

    df = pd.read_csv(DATA_FILE)

    if df.empty:

        st.warning("Training dataset is empty.")

        return

    # Convert collection time
    df["collected_at_utc"] = pd.to_datetime(
        df["collected_at_utc"],
        utc=True,
        errors="coerce"
    )

    # ==============================
    # DATASET METRICS
    # ==============================

    total_samples = len(df)

    total_regions = df["region"].nunique()

    missing_values = df.isnull().sum().sum()

    latest_collection = (
        df["collected_at_utc"]
        .max()
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "📊 Total Samples",
        total_samples
    )

    c2.metric(
        "🌍 Regions",
        total_regions
    )

    c3.metric(
        "⚠️ Missing Values",
        missing_values
    )

    if pd.notna(latest_collection):

        latest_text = latest_collection.strftime(
            "%d %b %Y"
        )

    else:

        latest_text = "Unknown"

    c4.metric(
        "🕒 Latest Collection",
        latest_text
    )

    st.divider()

    # ==============================
    # ML READINESS
    # ==============================

    st.subheader("🤖 ML Dataset Readiness")

    if total_samples < 100:

        progress = min(
            total_samples / 100,
            1.0
        )

        st.progress(progress)

        st.warning(
            f"Dataset not ready for ML experiments. "
            f"{total_samples}/100 prototype samples collected."
        )

        st.write(
            f"Collect approximately "
            f"**{100 - total_samples} more samples** "
            f"to reach the first experimental milestone."
        )

    elif total_samples < 500:

        st.progress(
            min(total_samples / 500, 1.0)
        )

        st.info(
            "Experimental ML testing can begin."
        )

        st.write(
            "More time-separated observations are still "
            "recommended before making strong model claims."
        )

    else:

        st.progress(1.0)

        st.success(
            "Dataset has reached the larger ML "
            "experiment milestone."
        )

    st.caption(
        "Sample-count milestones are project development "
        "targets, not proof of scientific or production readiness."
    )

    st.divider()

    # ==============================
    # REGION DISTRIBUTION
    # ==============================

    st.subheader("🌍 Samples by Region")

    region_counts = (
        df["region"]
        .value_counts()
        .reset_index()
    )

    region_counts.columns = [
        "Region",
        "Samples"
    ]

    region_fig = px.bar(
        region_counts,
        x="Region",
        y="Samples",
        color="Samples",
        title="Training Samples by Region"
    )

    st.plotly_chart(
        region_fig,
        use_container_width=True
    )

    st.divider()

    # ==============================
    # COLLECTION TIMELINE
    # ==============================

    st.subheader("📅 Dataset Collection Timeline")

    timeline_df = (
        df.dropna(
            subset=["collected_at_utc"]
        )
        .copy()
    )

    if not timeline_df.empty:

        timeline_df["Collection Date"] = (
            timeline_df[
                "collected_at_utc"
            ]
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

        timeline_fig = px.line(
            timeline_counts,
            x="Collection Date",
            y="Samples",
            markers=True,
            title="Environmental Dataset Growth"
        )

        st.plotly_chart(
            timeline_fig,
            use_container_width=True
        )

    else:

        st.info(
            "Collection timeline is unavailable."
        )

    st.divider()

    # ==============================
    # FEATURE STATISTICS
    # ==============================

    st.subheader("📊 Environmental Feature Statistics")

    feature_columns = [
        "hcho_mean",
        "aerosol_mean",
        "fire_detection_pixels",
        "surface_no2",
        "pm2_5",
        "pm10",
        "temperature",
        "humidity",
        "wind",
        "target_aqi_level"
    ]

    available_features = [
        column
        for column in feature_columns
        if column in df.columns
    ]

    statistics = (
        df[available_features]
        .describe()
        .round(5)
        .T
    )

    st.dataframe(
        statistics,
        use_container_width=True
    )

    st.divider()

    # ==============================
    # FEATURE EXPLORER
    # ==============================

    st.subheader("🔬 Feature Distribution Explorer")

    selected_feature = st.selectbox(
        "Select Environmental Feature",
        available_features
    )

    feature_fig = px.histogram(
        df,
        x=selected_feature,
        color="region",
        title=f"{selected_feature} Distribution"
    )

    st.plotly_chart(
        feature_fig,
        use_container_width=True
    )

    st.divider()

    # ==============================
    # MISSING DATA
    # ==============================

    st.subheader("🔎 Data Quality")

    missing_df = (
        df.isnull()
        .sum()
        .reset_index()
    )

    missing_df.columns = [
        "Feature",
        "Missing Values"
    ]

    missing_df = missing_df[
        missing_df["Missing Values"] > 0
    ]

    if missing_df.empty:

        st.success(
            "No missing values detected in the dataset."
        )

    else:

        st.warning(
            "Missing values detected."
        )

        st.dataframe(
            missing_df,
            use_container_width=True
        )

    st.divider()

    # ==============================
    # RAW DATA
    # ==============================

    with st.expander(
        "📂 View Training Dataset"
    ):

        st.dataframe(
            df,
            use_container_width=True
        )

        st.download_button(
            "📥 Download Training Dataset",
            data=df.to_csv(index=False),
            file_name=(
                "astraair_environmental_training_data.csv"
            ),
            mime="text/csv"
        )