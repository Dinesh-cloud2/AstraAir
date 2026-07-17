import ee

from satellite.gee import initialize_gee


REGION_CENTERS = {
    "India": [22.5, 79.0, 5],
    "Andaman and Nicobar": [11.74, 92.65, 7],
    "Andhra Pradesh": [15.91, 79.74, 6],
    "Arunachal Pradesh": [28.22, 94.73, 7],
    "Assam": [26.20, 92.94, 7],
    "Bihar": [25.96, 85.31, 7],
    "Chandigarh": [30.73, 76.78, 10],
    "Chhattisgarh": [21.28, 81.87, 7],
    "Dadra and Nagar Haveli": [20.18, 73.02, 9],
    "Daman and Diu": [20.43, 72.84, 9],
    "Delhi": [28.61, 77.21, 9],
    "Goa": [15.30, 74.12, 8],
    "Gujarat": [22.26, 71.19, 6],
    "Haryana": [29.05, 76.08, 7],
    "Himachal Pradesh": [31.10, 77.17, 7],
    "Jammu and Kashmir": [33.78, 76.58, 6],
    "Jharkhand": [23.61, 85.28, 7],
    "Karnataka": [15.32, 75.71, 6],
    "Kerala": [10.85, 76.27, 7],
    "Lakshadweep": [10.57, 72.64, 8],
    "Madhya Pradesh": [23.47, 77.95, 6],
    "Maharashtra": [19.75, 75.71, 6],
    "Manipur": [24.66, 93.91, 8],
    "Meghalaya": [25.47, 91.37, 8],
    "Mizoram": [23.16, 92.94, 8],
    "Nagaland": [26.16, 94.56, 8],
    "Odisha": [20.95, 85.10, 7],
    "Puducherry": [11.94, 79.81, 9],
    "Punjab": [31.15, 75.34, 7],
    "Rajasthan": [27.02, 74.22, 6],
    "Sikkim": [27.53, 88.51, 9],
    "Tamil Nadu": [11.13, 78.66, 7],
    "Telangana": [18.11, 79.02, 7],
    "Tripura": [23.94, 91.99, 8],
    "Uttar Pradesh": [26.85, 80.95, 6],
    "Uttarakhand": [30.07, 79.02, 7],
    "West Bengal": [22.99, 87.85, 7],
}


def get_india_states():
    initialize_gee()

    boundaries = ee.FeatureCollection(
        "FAO/GAUL/2015/level1"
    )

    return boundaries.filter(
        ee.Filter.eq("ADM0_NAME", "India")
    )


def get_region_names():
    india_states = get_india_states()

    names = (
        india_states
        .aggregate_array("ADM1_NAME")
        .distinct()
        .sort()
        .getInfo()
    )

    return ["India"] + names


def get_region_geometry(region_name):
    india_states = get_india_states()

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


def get_region_center(region_name):
    if region_name in REGION_CENTERS:
        return REGION_CENTERS[region_name]

    # Automatically calculate map centre
    geometry = get_region_geometry(region_name)

    coordinates = (
        geometry
        .centroid(maxError=1000)
        .coordinates()
        .getInfo()
    )

    longitude = coordinates[0]
    latitude = coordinates[1]

    return [latitude, longitude, 7]