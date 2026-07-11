import ee

from satellite.gee import initialize_gee


def get_aerosol_tile_url(start_date, end_date):

    initialize_gee()

    india = ee.Geometry.Rectangle([
        68.0,
        6.0,
        97.5,
        37.5
    ])

    collection = (
        ee.ImageCollection("COPERNICUS/S5P/OFFL/L3_AER_AI")
        .select("absorbing_aerosol_index")
        .filterDate(start_date, end_date)
        .filterBounds(india)
    )

    image_count = collection.size().getInfo()

    if image_count == 0:
        return None, 0

    image = collection.mean().clip(india)

    vis_params = {
        "min": -1.0,
        "max": 3.0,
        "palette": [
            "0000ff",
            "00ffff",
            "00ff00",
            "ffff00",
            "ff8800",
            "ff0000"
        ]
    }

    map_id = image.getMapId(vis_params)
    tile_url = map_id["tile_fetcher"].url_format

    return tile_url, image_count