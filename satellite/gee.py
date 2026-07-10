import ee

PROJECT_ID = "isro-aqi-project-501317"


def initialize_gee():
    try:
        ee.Initialize(project=PROJECT_ID)
        print("✅ Google Earth Engine Connected")
    except Exception:
        ee.Authenticate()
        ee.Initialize(project=PROJECT_ID)
        print("✅ Google Earth Engine Authenticated")