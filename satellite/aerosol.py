import ee

from satellite.gee import initialize_gee
from satellite.regions import get_region_geometry


def get_aerosol_tile_url(
    start_date,
    end_date,
    region_name="India"
):

    initialize_gee()

    region = get_region_geometry(region_name)

    collection = (
        ee.ImageCollection(
            "COPERNICUS/S5P/OFFL/L3_AER_AI"
        )
        .select(
            "absorbing_aerosol_index"
        )
        .filterDate(start_date, end_date)
        .filterBounds(region)
    )

    image_count = collection.size().getInfo()

    if image_count == 0:
        return None, 0

    image = collection.mean().clip(region)

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

    tile_url = map_id[
        "tile_fetcher"
    ].url_format

    return tile_url, image_count