from services.aqi import get_live_aqi
from services.weather import get_weather
from services.satellite_intelligence import (
    get_satellite_evidence,
    generate_satellite_interpretation,
)


REGION_LOCATIONS = {
    "India": [
        ("Delhi", 28.6139, 77.2090),
        ("Mumbai", 19.0760, 72.8777),
        ("Bengaluru", 12.9716, 77.5946),
        ("Kolkata", 22.5726, 88.3639),
    ],

    "Delhi": [
        ("Delhi", 28.6139, 77.2090),
    ],

    "Punjab": [
        ("Ludhiana", 30.9010, 75.8573),
        ("Amritsar", 31.6340, 74.8723),
        ("Patiala", 30.3398, 76.3869),
    ],

    "Haryana": [
        ("Gurugram", 28.4595, 77.0266),
        ("Faridabad", 28.4089, 77.3178),
        ("Hisar", 29.1492, 75.7217),
    ],

    "Uttar Pradesh": [
        ("Lucknow", 26.8467, 80.9462),
        ("Kanpur", 26.4499, 80.3319),
        ("Varanasi", 25.3176, 82.9739),
    ],

    "Bihar": [
        ("Patna", 25.5941, 85.1376),
        ("Gaya", 24.7914, 85.0002),
        ("Muzaffarpur", 26.1209, 85.3647),
    ],
}


def safe_average(values, digits=2):
    valid_values = [
        float(value)
        for value in values
        if value is not None
    ]

    if not valid_values:
        return 0.0

    return round(
        sum(valid_values) / len(valid_values),
        digits,
    )


def get_live_region_data(region_name):
    locations = REGION_LOCATIONS.get(
        region_name,
        REGION_LOCATIONS["India"],
    )

    rows = []

    for city, latitude, longitude in locations:
        air = get_live_aqi(latitude, longitude)
        weather = get_weather(city)

        if air:
            rows.append({
                "city": city,
                "aqi": air["aqi"],
                "pm2_5": air["pm2_5"],
                "pm10": air["pm10"],
                "no2": air["no2"],
                "o3": air["o3"],
                "co": air["co"],
                "temperature": (
                    weather["temperature"]
                    if weather else None
                ),
                "humidity": (
                    weather["humidity"]
                    if weather else None
                ),
                "wind": (
                    weather["wind"]
                    if weather else None
                ),
            })

    if not rows:
        return None

    return {
        "locations": rows,
        "average_aqi": safe_average(
            [row["aqi"] for row in rows]
        ),
        "average_pm2_5": safe_average(
            [row["pm2_5"] for row in rows]
        ),
        "average_pm10": safe_average(
            [row["pm10"] for row in rows]
        ),
        "average_no2": safe_average(
            [row["no2"] for row in rows]
        ),
        "average_temperature": safe_average(
            [row["temperature"] for row in rows]
        ),
        "average_humidity": safe_average(
            [row["humidity"] for row in rows]
        ),
        "average_wind": safe_average(
            [row["wind"] for row in rows]
        ),
    }


def generate_fusion_interpretation(
    satellite_evidence,
    live_data,
):
    signals = []

    if satellite_evidence["hcho_mean"] > 0.00015:
        signals.append(
            "Elevated satellite HCHO signal"
        )

    if satellite_evidence["aerosol_mean"] > 1.0:
        signals.append(
            "Elevated absorbing aerosol signal"
        )

    if satellite_evidence["fire_detection_pixels"] > 0:
        signals.append(
            "Active-fire satellite evidence"
        )

    if live_data["average_aqi"] >= 4:
        signals.append(
            "Poor live AQI conditions"
        )

    if live_data["average_pm2_5"] > 35:
        signals.append(
            "Elevated surface PM2.5"
        )

    if live_data["average_pm10"] > 50:
        signals.append(
            "Elevated surface PM10"
        )

    if live_data["average_wind"] < 3:
        signals.append(
            "Low wind may limit pollutant dispersion"
        )

    if live_data["average_humidity"] > 75:
        signals.append(
            "High humidity may support pollutant accumulation"
        )

    count = len(signals)

    if count >= 6:
        level = "High Environmental Concern"

        summary = (
            "Multiple satellite, air-quality and weather "
            "indicators are simultaneously elevated. "
            "The selected region may be experiencing a "
            "significant pollution episode."
        )

    elif count >= 3:
        level = "Moderate Environmental Concern"

        summary = (
            "Several environmental indicators are present. "
            "Pollution conditions should be monitored and "
            "compared with local ground-station information."
        )

    elif count >= 1:
        level = "Limited Environmental Concern"

        summary = (
            "Some indicators are elevated, but the combined "
            "evidence is not strong enough to identify a "
            "major regional pollution episode."
        )

    else:
        level = "Low Environmental Concern"

        summary = (
            "Satellite observations, live AQI and weather "
            "conditions do not show strong combined pollution "
            "evidence for the selected period."
        )

    return {
        "level": level,
        "signals": signals,
        "summary": summary,
    }


def get_environmental_fusion(
    start_date,
    end_date,
    region_name,
):
    satellite_evidence = get_satellite_evidence(
        start_date,
        end_date,
        region_name,
    )

    live_data = get_live_region_data(region_name)

    if satellite_evidence is None or live_data is None:
        return None

    satellite_analysis = (
        generate_satellite_interpretation(
            satellite_evidence
        )
    )

    fusion_analysis = generate_fusion_interpretation(
        satellite_evidence,
        live_data,
    )

    return {
        "satellite": satellite_evidence,
        "satellite_analysis": satellite_analysis,
        "live": live_data,
        "fusion": fusion_analysis,
    }