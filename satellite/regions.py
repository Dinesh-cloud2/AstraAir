
import ee


SUPPORTED_REGIONS = [
    "India",
    "Delhi",
    "Punjab",
    "Haryana",
    "Uttar Pradesh",
    "Bihar",
]


REGION_CENTERS = {
    "India": [22.5, 79.0, 5],
    "Delhi": [28.61, 77.21, 9],
    "Punjab": [31.15, 75.34, 7],
    "Haryana": [29.05, 76.08, 7],
    "Uttar Pradesh": [26.85, 80.95, 6],
    "Bihar": [25.96, 85.31, 7],
}


def get_region_names():
    return SUPPORTED_REGIONS


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

    return selected_region.geometry()


def get_region_center(region_name):

    return REGION_CENTERS.get(
        region_name,
        REGION_CENTERS["India"]
    )