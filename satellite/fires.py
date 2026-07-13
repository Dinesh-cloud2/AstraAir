import ee

from satellite.gee import initialize_gee
from satellite.regions import get_region_geometry


def get_fire_tile_url(
    start_date,
    end_date,
    region_name="India"
):

    initialize_gee()

    region = get_region_geometry(region_name)

    collection = (
        ee.ImageCollection("FIRMS")
        .select("T21")
        .filterDate(start_date, end_date)
        .filterBounds(region)
    )

    image_count = collection.size().getInfo()

    if image_count == 0:
        return None, 0

    fire_image = (
        collection
        .max()
        .clip(region)
    )

    vis_params = {
        "min": 325.0,
        "max": 400.0,
        "palette": [
            "ffff00",
            "ff8800",
            "ff0000"
        ]
    }

    map_id = fire_image.getMapId(
        vis_params
    )

    tile_url = map_id[
        "tile_fetcher"
    ].url_format

    return tile_url, image_count