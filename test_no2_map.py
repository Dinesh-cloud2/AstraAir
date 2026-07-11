import ee
import folium
from satellite.gee import initialize_gee

initialize_gee()

india = ee.Geometry.Rectangle([68.0, 6.0, 97.5, 37.5])

collection = (
    ee.ImageCollection("COPERNICUS/S5P/OFFL/L3_NO2")
    .select("tropospheric_NO2_column_number_density")
    .filterDate("2025-07-01", "2025-07-10")
    .filterBounds(india)
)

count = collection.size().getInfo()
print("Images found:", count)

if count == 0:
    raise ValueError("No Sentinel-5P NO2 images found.")

image = collection.mean().clip(india)

vis_params = {
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
}

map_id = image.getMapId(vis_params)
tile_url = map_id["tile_fetcher"].url_format

m = folium.Map(
    location=[22.5, 79.0],
    zoom_start=5,
    tiles="CartoDB positron",
)

folium.TileLayer(
    tiles=tile_url,
    attr="Google Earth Engine / Sentinel-5P",
    name="Sentinel-5P NO2",
    overlay=True,
    control=True,
).add_to(m)

folium.LayerControl().add_to(m)

output_file = "no2_india_map.html"
m.save(output_file)

print(f"Map created successfully: {output_file}")