import ee

from satellite.gee import initialize_gee

initialize_gee()


def get_no2_tile_url(start_date, end_date, opacity=0.75):
    india = ee.Geometry.Rectangle([68.0, 6.0, 97.5, 37.5])

    collection = (
        ee.ImageCollection("COPERNICUS/S5P/OFFL/L3_NO2")
        .select("tropospheric_NO2_column_number_density")
        .filterDate(start_date, end_date)
        .filterBounds(india)
    )

    image_count = collection.size().getInfo()

    if image_count == 0:
        return None, 0

    image = collection.mean().clip(india)

    visualization = {
        "min": 0.0,
        "max": 0.0002,
        "palette": [
            "0000ff",
            "00ffff",
            "00ff00",
            "ffff00",
            "ff7f00",
            "ff0000",
        ],
        "opacity": opacity,
    }

    map_id = image.getMapId(visualization)

    return map_id["tile_fetcher"].url_format, image_count