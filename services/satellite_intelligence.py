import ee

from satellite.gee import initialize_gee


SUPPORTED_REGIONS = [
    "India",
    "Delhi",
    "Punjab",
    "Haryana",
    "Uttar Pradesh",
    "Bihar",
]


def get_region_names():
    return SUPPORTED_REGIONS


def safe_number(value, digits=6):
    if value is None:
        return 0.0

    return round(float(value), digits)


def get_region_geometry(region_name):
    boundaries = ee.FeatureCollection(
        "FAO/GAUL/2015/level1"
    )

    india_states = boundaries.filter(
        ee.Filter.eq("ADM0_NAME", "India")
    )

    if region_name == "India":
        return india_states.geometry()

    selected_region = india_states.filter(
        ee.Filter.eq("ADM1_NAME", region_name)
    )

    region_count = selected_region.size().getInfo()

    if region_count == 0:
        raise ValueError(
            f"Boundary not found for region: {region_name}"
        )

    return selected_region.geometry()


def get_satellite_evidence(
    start_date,
    end_date,
    region_name="India",
):
    initialize_gee()

    region = get_region_geometry(region_name)

    hcho_collection = (
        ee.ImageCollection(
            "COPERNICUS/S5P/OFFL/L3_HCHO"
        )
        .select(
            "tropospheric_HCHO_column_number_density"
        )
        .filterDate(start_date, end_date)
        .filterBounds(region)
    )

    aerosol_collection = (
        ee.ImageCollection(
            "COPERNICUS/S5P/OFFL/L3_AER_AI"
        )
        .select("absorbing_aerosol_index")
        .filterDate(start_date, end_date)
        .filterBounds(region)
    )

    fire_collection = (
        ee.ImageCollection("FIRMS")
        .select(["T21", "confidence"])
        .filterDate(start_date, end_date)
        .filterBounds(region)
    )

    hcho_image_count = hcho_collection.size().getInfo()
    aerosol_image_count = aerosol_collection.size().getInfo()
    fire_image_count = fire_collection.size().getInfo()

    if hcho_image_count == 0 or aerosol_image_count == 0:
        return None

    hcho_stats = hcho_collection.mean().reduceRegion(
        reducer=ee.Reducer.mean(),
        geometry=region,
        scale=10000,
        maxPixels=1e9,
        bestEffort=True,
    ).getInfo()

    aerosol_stats = aerosol_collection.mean().reduceRegion(
        reducer=ee.Reducer.mean(),
        geometry=region,
        scale=10000,
        maxPixels=1e9,
        bestEffort=True,
    ).getInfo()

    hcho_mean = safe_number(
        hcho_stats.get(
            "tropospheric_HCHO_column_number_density"
        )
    )

    aerosol_mean = safe_number(
        aerosol_stats.get(
            "absorbing_aerosol_index"
        ),
        digits=3,
    )

    fire_detection_pixels = 0

    if fire_image_count > 0:
        fire_image = fire_collection.max()

        fire_mask = (
            fire_image.select("T21")
            .gt(325)
            .And(
                fire_image.select("confidence").gte(30)
            )
            .selfMask()
        )

        fire_stats = fire_mask.reduceRegion(
            reducer=ee.Reducer.count(),
            geometry=region,
            scale=1000,
            maxPixels=1e9,
            bestEffort=True,
        ).getInfo()

        fire_detection_pixels = int(
            fire_stats.get("T21", 0) or 0
        )

    return {
        "region": region_name,
        "hcho_mean": hcho_mean,
        "aerosol_mean": aerosol_mean,
        "fire_detection_pixels": fire_detection_pixels,
        "hcho_image_count": hcho_image_count,
        "aerosol_image_count": aerosol_image_count,
        "fire_image_count": fire_image_count,
    }


def generate_satellite_interpretation(evidence):
    hcho = evidence["hcho_mean"]
    aerosol = evidence["aerosol_mean"]
    fires = evidence["fire_detection_pixels"]
    region = evidence["region"]

    signals = []

    if hcho > 0.00015:
        signals.append("Elevated HCHO signal")

    if aerosol > 1.0:
        signals.append(
            "Elevated absorbing aerosol signal"
        )

    if fires > 0:
        signals.append(
            "Active-fire detection evidence"
        )

    signal_count = len(signals)

    if signal_count == 3:
        level = "Strong Multi-Signal Evidence"

        interpretation = (
            f"HCHO, absorbing aerosol and active-fire "
            f"signals are simultaneously present over {region}. "
            "The combined evidence may indicate possible "
            "biomass-burning influence. Ground validation "
            "is recommended."
        )

    elif signal_count == 2:
        level = "Moderate Multi-Signal Evidence"

        interpretation = (
            f"Multiple satellite indicators are present over "
            f"{region}. Possible biomass-burning influence "
            "should be investigated using regional weather, "
            "ground AQI and emission-source information."
        )

    elif signal_count == 1:
        level = "Limited Satellite Evidence"

        interpretation = (
            f"Only one satellite indicator is elevated over "
            f"{region}. The available evidence is insufficient "
            "to identify a particular pollution source."
        )

    else:
        level = "Low Multi-Signal Evidence"

        interpretation = (
            f"The selected period does not show strong combined "
            f"HCHO, aerosol and active-fire evidence over "
            f"{region}."
        )

    return {
        "level": level,
        "signals": signals,
        "interpretation": interpretation,
    }