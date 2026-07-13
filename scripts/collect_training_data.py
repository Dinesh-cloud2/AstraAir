from datetime import datetime, timedelta, timezone
from pathlib import Path

import pandas as pd

from services.environmental_fusion import get_live_region_data
from services.satellite_intelligence import get_satellite_evidence


REGIONS = [
    "India",
    "Delhi",
    "Punjab",
    "Haryana",
    "Uttar Pradesh",
    "Bihar",
]

OUTPUT_FILE = Path(
    "data/training/environmental_training_data.csv"
)


def build_region_record(
    region_name: str,
    satellite_start: str,
    satellite_end: str,
) -> dict | None:
    """
    Build one time-aligned regional training record.

    The live API supplies the prediction target and surface features.
    Satellite features are calculated over the recent date window.
    """

    satellite = get_satellite_evidence(
        satellite_start,
        satellite_end,
        region_name,
    )

    live = get_live_region_data(region_name)

    if satellite is None or live is None:
        print(f"Skipped {region_name}: data unavailable")
        return None

    return {
        "collected_at_utc": datetime.now(
            timezone.utc
        ).isoformat(),

        "region": region_name,

        # Satellite features
        "satellite_start": satellite_start,
        "satellite_end": satellite_end,
        "hcho_mean": satellite["hcho_mean"],
        "aerosol_mean": satellite["aerosol_mean"],
        "fire_detection_pixels": satellite[
            "fire_detection_pixels"
        ],

        # Surface pollution features
        "surface_no2": live["average_no2"],
        "pm2_5": live["average_pm2_5"],
        "pm10": live["average_pm10"],

        # Weather features
        "temperature": live["average_temperature"],
        "humidity": live["average_humidity"],
        "wind": live["average_wind"],

        # Initial prediction target:
        # OpenWeather AQI category from 1 to 5
        "target_aqi_level": live["average_aqi"],

        # Observation metadata
        "sampled_locations": len(live["locations"]),
        "hcho_image_count": satellite[
            "hcho_image_count"
        ],
        "aerosol_image_count": satellite[
            "aerosol_image_count"
        ],
        "fire_image_count": satellite[
            "fire_image_count"
        ],
    }


def remove_duplicate_snapshots(
    dataframe: pd.DataFrame,
) -> pd.DataFrame:
    """
    Avoid repeated rows if the collector is accidentally
    executed multiple times within the same hour.
    """

    dataframe["snapshot_hour"] = pd.to_datetime(
        dataframe["collected_at_utc"],
        utc=True,
    ).dt.floor("h")

    dataframe = dataframe.drop_duplicates(
        subset=["region", "snapshot_hour"],
        keep="last",
    )

    return dataframe.drop(
        columns=["snapshot_hour"]
    )


def collect_training_snapshot() -> None:
    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    # Use the most recent completed seven-day satellite window.
    # A short delay helps avoid selecting dates for which
    # satellite products are not yet available.
    satellite_end_date = (
        datetime.now(timezone.utc).date()
        - timedelta(days=3)
    )

    satellite_start_date = (
        satellite_end_date
        - timedelta(days=7)
    )

    satellite_start = satellite_start_date.isoformat()
    satellite_end = satellite_end_date.isoformat()

    print(
        "Satellite window:",
        satellite_start,
        "to",
        satellite_end,
    )

    new_records = []

    for region in REGIONS:
        print(f"Collecting: {region}")

        try:
            record = build_region_record(
                region,
                satellite_start,
                satellite_end,
            )

            if record is not None:
                new_records.append(record)

        except Exception as error:
            print(
                f"Failed for {region}: "
                f"{type(error).__name__}: {error}"
            )

    if not new_records:
        print("No records collected.")
        return

    new_dataframe = pd.DataFrame(new_records)

    if OUTPUT_FILE.exists():
        old_dataframe = pd.read_csv(OUTPUT_FILE)

        final_dataframe = pd.concat(
            [old_dataframe, new_dataframe],
            ignore_index=True,
        )

    else:
        final_dataframe = new_dataframe

    final_dataframe = remove_duplicate_snapshots(
        final_dataframe
    )

    final_dataframe.to_csv(
        OUTPUT_FILE,
        index=False,
    )

    print(
        f"Saved {len(new_records)} new records."
    )
    print(
        f"Total dataset rows: "
        f"{len(final_dataframe)}"
    )
    print(
        f"Dataset: {OUTPUT_FILE.resolve()}"
    )


if __name__ == "__main__":
    collect_training_snapshot()