import ee

from satellite.gee import initialize_gee


def get_fire_tile_url(start_date, end_date):
    initialize_gee()

    india = ee.Geometry.Rectangle([
        68.0,
        6.0,
        97.5,
        37.5,
    ])

    collection = (
        ee.ImageCollection("FIRMS")
        .select("T21")
        .filterDate(start_date, end_date)
        .filterBounds(india)
    )

    image_count = collection.size().getInfo()

    if image_count == 0:
        return None, 0

    fire_image = collection.max().clip(india)

    vis_params = {
        "min": 325.0,
        "max": 400.0,
        "palette": [
            "ffff00",
            "ff8800",
            "ff0000",
        ],
    }

    map_id = fire_image.getMapId(vis_params)
    tile_url = map_id["tile_fetcher"].url_format

    return tile_url, image_count