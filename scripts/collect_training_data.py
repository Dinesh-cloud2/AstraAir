from datetime import datetime, timedelta, timezone
from pathlib import Path
from time import sleep

import pandas as pd

from services.aqi import get_live_aqi
from services.cities import get_cities
from services.satellite_intelligence import (
    get_satellite_evidence,
)
from services.weather import get_weather


OUTPUT_FILE = Path(
    "data/training/environmental_training_data.csv"
)

# Small delay between cities to avoid hitting API too quickly.
API_DELAY_SECONDS = 0.15


def safe_value(data, key, default=None):
    """
    Safely read a value from a dictionary.
    """

    if not data:
        return default

    return data.get(key, default)


def get_satellite_window():
    """
    Use the latest completed seven-day satellite window.

    A three-day delay reduces the chance of selecting
    dates whose satellite products are not yet available.
    """

    satellite_end_date = (
        datetime.now(timezone.utc).date()
        - timedelta(days=3)
    )

    satellite_start_date = (
        satellite_end_date
        - timedelta(days=7)
    )

    return (
        satellite_start_date.isoformat(),
        satellite_end_date.isoformat(),
    )


def load_state_satellite_evidence(
    state_name,
    satellite_start,
    satellite_end,
    cache,
):
    """
    Calculate satellite evidence once per state.

    The result is cached so multiple cities in the same
    state do not trigger repeated Earth Engine processing.
    """

    if state_name in cache:
        return cache[state_name]

    print(
        f"  Satellite evidence: {state_name}"
    )

    try:
        evidence = get_satellite_evidence(
            satellite_start,
            satellite_end,
            state_name,
        )

    except Exception as error:
        print(
            f"  Satellite unavailable for {state_name}: "
            f"{type(error).__name__}: {error}"
        )

        evidence = None

    cache[state_name] = evidence

    return evidence


def build_city_record(
    city,
    state,
    latitude,
    longitude,
    satellite_start,
    satellite_end,
    satellite_cache,
):
    """
    Build one city-level environmental training record.
    """

    # Current air-pollution observation
    air = get_live_aqi(
        latitude,
        longitude,
    )

    if not air:
        print(
            f"  Skipped {city}: AQI data unavailable"
        )
        return None

    # Current weather observation
    weather = get_weather(
        city=city,
        lat=latitude,
        lon=longitude,
    )

    if not weather:
        print(
            f"  Skipped {city}: weather data unavailable"
        )
        return None

    # Regional satellite features are reused
    # for all cities within the same state.
    satellite = load_state_satellite_evidence(
        state_name=state,
        satellite_start=satellite_start,
        satellite_end=satellite_end,
        cache=satellite_cache,
    )

    if satellite is None:
        print(
            f"  Skipped {city}: "
            f"satellite data unavailable for {state}"
        )
        return None

    collected_at = datetime.now(
        timezone.utc
    ).isoformat()

    record = {
        # Collection metadata
        "collected_at_utc": collected_at,
        "city": city,
        "state": state,

        # Keep region for compatibility with the
        # Training Data dashboard.
        "region": city,

        "latitude": latitude,
        "longitude": longitude,

        # Satellite time window
        "satellite_start": satellite_start,
        "satellite_end": satellite_end,

        # Satellite features
        "hcho_mean": safe_value(
            satellite,
            "hcho_mean",
        ),

        "aerosol_mean": safe_value(
            satellite,
            "aerosol_mean",
        ),

        "fire_detection_pixels": safe_value(
            satellite,
            "fire_detection_pixels",
        ),

        # Surface pollutant features
        "surface_no2": safe_value(
            air,
            "no2",
        ),

        "pm2_5": safe_value(
            air,
            "pm2_5",
        ),

        "pm10": safe_value(
            air,
            "pm10",
        ),

        "o3": safe_value(
            air,
            "o3",
        ),

        "co": safe_value(
            air,
            "co",
        ),

        # Weather features
        "temperature": safe_value(
            weather,
            "temperature",
        ),

        "humidity": safe_value(
            weather,
            "humidity",
        ),

        "wind": safe_value(
            weather,
            "wind",
        ),

        "weather_description": safe_value(
            weather,
            "description",
        ),

        # Initial ML target:
        # OpenWeather AQI category from 1 to 5.
        "target_aqi_level": safe_value(
            air,
            "aqi",
        ),

        # Satellite observation metadata
        "hcho_image_count": safe_value(
            satellite,
            "hcho_image_count",
            0,
        ),

        "aerosol_image_count": safe_value(
            satellite,
            "aerosol_image_count",
            0,
        ),

        "fire_image_count": safe_value(
            satellite,
            "fire_image_count",
            0,
        ),

        # One city is sampled in this record.
        "sampled_locations": 1,
    }

    return record


def remove_duplicate_snapshots(
    dataframe,
):
    """
    Prevent multiple records for the same city
    within the same UTC hour.
    """

    if dataframe.empty:
        return dataframe

    dataframe["collected_at_utc"] = pd.to_datetime(
        dataframe["collected_at_utc"],
        utc=True,
        errors="coerce",
    )

    dataframe["snapshot_hour"] = (
        dataframe["collected_at_utc"]
        .dt.floor("h")
    )

    # Support both new and older dataset records.
    if "city" not in dataframe.columns:
        dataframe["city"] = dataframe.get(
            "region",
            "Unknown",
        )

    dataframe = dataframe.drop_duplicates(
        subset=[
            "city",
            "snapshot_hour",
        ],
        keep="last",
    )

    dataframe = dataframe.drop(
        columns=["snapshot_hour"],
        errors="ignore",
    )

    dataframe["collected_at_utc"] = (
        dataframe["collected_at_utc"]
        .astype(str)
    )

    return dataframe


def collect_training_snapshot():
    """
    Collect one current record for every city
    available in data/cities.csv.
    """

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    cities_df = get_cities().copy()

    if cities_df.empty:
        print("City dataset is empty.")
        return

    required_city_columns = [
        "City",
        "State",
        "Latitude",
        "Longitude",
    ]

    missing_columns = [
        column
        for column in required_city_columns
        if column not in cities_df.columns
    ]

    if missing_columns:
        print(
            "Missing city columns:",
            ", ".join(missing_columns),
        )
        return

    (
        satellite_start,
        satellite_end,
    ) = get_satellite_window()

    print("=" * 60)
    print("ASTRAAIR CITY DATA COLLECTION")
    print("=" * 60)

    print(
        "Satellite window:",
        satellite_start,
        "to",
        satellite_end,
    )

    print(
        "Cities available:",
        len(cities_df),
    )

    new_records = []

    failed_cities = []

    satellite_cache = {}

    total_cities = len(cities_df)

    for index, (_, row) in enumerate(
        cities_df.iterrows(),
        start=1,
    ):
        city = str(row["City"]).strip()
        state = str(row["State"]).strip()

        latitude = float(
            row["Latitude"]
        )

        longitude = float(
            row["Longitude"]
        )

        print(
            f"\n[{index}/{total_cities}] "
            f"Collecting: {city}, {state}"
        )

        try:
            record = build_city_record(
                city=city,
                state=state,
                latitude=latitude,
                longitude=longitude,
                satellite_start=satellite_start,
                satellite_end=satellite_end,
                satellite_cache=satellite_cache,
            )

            if record is not None:
                new_records.append(record)

                print(
                    f"  Success: AQI "
                    f"{record['target_aqi_level']}/5"
                )

            else:
                failed_cities.append(
                    f"{city}, {state}"
                )

        except Exception as error:
            failed_cities.append(
                f"{city}, {state}"
            )

            print(
                f"  Failed: "
                f"{type(error).__name__}: {error}"
            )

        sleep(API_DELAY_SECONDS)

    if not new_records:
        print("\nNo new records were collected.")
        return

    new_dataframe = pd.DataFrame(
        new_records
    )

    if OUTPUT_FILE.exists():
        try:
            old_dataframe = pd.read_csv(
                OUTPUT_FILE
            )

            final_dataframe = pd.concat(
                [
                    old_dataframe,
                    new_dataframe,
                ],
                ignore_index=True,
                sort=False,
            )

        except Exception as error:
            print(
                "Existing dataset could not be read:",
                error,
            )

            print(
                "A new dataset will be created."
            )

            final_dataframe = new_dataframe

    else:
        final_dataframe = new_dataframe

    final_dataframe = remove_duplicate_snapshots(
        final_dataframe
    )

    final_dataframe.to_csv(
        OUTPUT_FILE,
        index=False,
        encoding="utf-8",
    )

    print("\n" + "=" * 60)
    print("COLLECTION COMPLETE")
    print("=" * 60)

    print(
        f"Cities processed: {total_cities}"
    )

    print(
        f"Successful records: "
        f"{len(new_records)}"
    )

    print(
        f"Failed cities: "
        f"{len(failed_cities)}"
    )

    print(
        f"Total dataset rows: "
        f"{len(final_dataframe)}"
    )

    print(
        f"Dataset saved at: "
        f"{OUTPUT_FILE.resolve()}"
    )

    if failed_cities:
        print("\nFailed city list:")

        for city_name in failed_cities:
            print(
                f"  - {city_name}"
            )


if __name__ == "__main__":
    collect_training_snapshot()