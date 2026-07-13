from pathlib import Path

import pandas as pd


DATA_FILE = Path(
    "data/training/environmental_training_data.csv"
)


REQUIRED_COLUMNS = [
    "region",
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


def validate_dataset():

    if not DATA_FILE.exists():
        print("❌ Training dataset not found.")
        return

    df = pd.read_csv(DATA_FILE)

    print("\n🌍 ASTRAAIR DATASET VALIDATION")
    print("=" * 45)

    print(f"\nTotal Rows: {len(df)}")
    print(f"Total Columns: {len(df.columns)}")

    print("\n📍 Regions")

    print(
        df["region"]
        .value_counts()
        .to_string()
    )

    print("\n🔎 Missing Values")

    missing = df[
        REQUIRED_COLUMNS
    ].isnull().sum()

    print(missing.to_string())

    print("\n📋 Duplicate Rows")

    duplicate_count = df.duplicated().sum()

    print(
        f"Duplicate rows: {duplicate_count}"
    )

    print("\n📊 Feature Statistics")

    numeric_columns = [
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

    print(
        df[numeric_columns]
        .describe()
        .round(4)
        .to_string()
    )

    print("\n⚠️ Range Validation")

    problems = []

    if (df["humidity"] < 0).any():
        problems.append(
            "Humidity below 0 detected."
        )

    if (df["humidity"] > 100).any():
        problems.append(
            "Humidity above 100 detected."
        )

    if (df["wind"] < 0).any():
        problems.append(
            "Negative wind speed detected."
        )

    if (df["pm2_5"] < 0).any():
        problems.append(
            "Negative PM2.5 detected."
        )

    if (df["pm10"] < 0).any():
        problems.append(
            "Negative PM10 detected."
        )

    if (
        (df["target_aqi_level"] < 1).any()
        or
        (df["target_aqi_level"] > 5).any()
    ):
        problems.append(
            "AQI target outside 1-5 detected."
        )

    if problems:

        print("\n❌ Validation Problems")

        for problem in problems:
            print(f"- {problem}")

    else:

        print(
            "\n✅ No basic range problems detected."
        )

    print("\n🤖 ML Readiness")

    if len(df) < 100:

        print(
            "❌ NOT READY FOR ML"
        )

        print(
            "Recommended: collect at least "
            "100 time-separated observations."
        )

    elif len(df) < 500:

        print(
            "⚠️ EXPERIMENTAL ML READY"
        )

        print(
            "Model testing can begin, but "
            "more observations are recommended."
        )

    else:

        print(
            "✅ DATASET READY FOR ML EXPERIMENTS"
        )

    print("\n" + "=" * 45)


if __name__ == "__main__":
    validate_dataset()