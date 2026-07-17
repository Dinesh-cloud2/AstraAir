def calculate_sub_index(
    concentration,
    breakpoints,
):
    """
    Calculate AQI sub-index using linear interpolation.

    Each breakpoint:
    (concentration_low, concentration_high,
     aqi_low, aqi_high)
    """

    concentration = float(concentration)

    for (
        concentration_low,
        concentration_high,
        aqi_low,
        aqi_high,
    ) in breakpoints:

        if concentration_low <= concentration <= concentration_high:

            sub_index = (
                (aqi_high - aqi_low)
                / (concentration_high - concentration_low)
                * (concentration - concentration_low)
                + aqi_low
            )

            return round(sub_index)

    # Concentration above final breakpoint
    return 500


PM25_BREAKPOINTS = [
    (0, 30, 0, 50),
    (31, 60, 51, 100),
    (61, 90, 101, 200),
    (91, 120, 201, 300),
    (121, 250, 301, 400),
    (251, 500, 401, 500),
]


PM10_BREAKPOINTS = [
    (0, 50, 0, 50),
    (51, 100, 51, 100),
    (101, 250, 101, 200),
    (251, 350, 201, 300),
    (351, 430, 301, 400),
    (431, 600, 401, 500),
]


def calculate_indian_aqi(pm2_5, pm10):
    pm25_sub_index = calculate_sub_index(
        pm2_5,
        PM25_BREAKPOINTS,
    )

    pm10_sub_index = calculate_sub_index(
        pm10,
        PM10_BREAKPOINTS,
    )

    estimated_aqi = max(
        pm25_sub_index,
        pm10_sub_index,
    )

    dominant_pollutant = (
        "PM2.5"
        if pm25_sub_index >= pm10_sub_index
        else "PM10"
    )

    return {
        "aqi": estimated_aqi,
        "dominant_pollutant": dominant_pollutant,
        "pm2_5_sub_index": pm25_sub_index,
        "pm10_sub_index": pm10_sub_index,
    }


def get_indian_aqi_category(aqi):
    if aqi <= 50:
        return "Good"

    if aqi <= 100:
        return "Satisfactory"

    if aqi <= 200:
        return "Moderately Polluted"

    if aqi <= 300:
        return "Poor"

    if aqi <= 400:
        return "Very Poor"

    return "Severe"


def get_indian_aqi_color(aqi):
    if aqi <= 50:
        return "green"

    if aqi <= 100:
        return "lightgreen"

    if aqi <= 200:
        return "orange"

    if aqi <= 300:
        return "red"

    if aqi <= 400:
        return "purple"

    return "darkred"


def get_indian_health_advice(aqi):
    if aqi <= 50:
        return (
            "Air quality appears good. Normal outdoor "
            "activities are generally suitable."
        )

    if aqi <= 100:
        return (
            "Air quality appears satisfactory. Sensitive "
            "people may monitor prolonged outdoor exposure."
        )

    if aqi <= 200:
        return (
            "Sensitive groups should reduce prolonged "
            "or strenuous outdoor activity."
        )

    if aqi <= 300:
        return (
            "Reduce outdoor exercise. Consider using a "
            "well-fitting protective mask."
        )

    if aqi <= 400:
        return (
            "Avoid prolonged outdoor exposure, especially "
            "for children, elderly people and sensitive groups."
        )

    return (
        "Avoid unnecessary outdoor exposure. Follow local "
        "public-health and pollution-control advisories."
    )