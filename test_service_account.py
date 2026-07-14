import ee

SERVICE_ACCOUNT = "astraair-earth-engine@isro-aqi-project-501317.iam.gserviceaccount.com"
PROJECT_ID = "isro-aqi-project-501317"

KEY_FILE = (
    r"C:\Users\Dinesh singh"
    r"\.astraair\earth-engine-key.json"
)

credentials = ee.ServiceAccountCredentials(
    SERVICE_ACCOUNT,
    KEY_FILE,
)

ee.Initialize(
    credentials,
    project=PROJECT_ID,
)

print("✅ Earth Engine Service Account Connected")

collection = ee.ImageCollection(
    "COPERNICUS/S5P/OFFL/L3_NO2"
)

print(
    "NO2 Images:",
    collection.limit(10).size().getInfo(),
)