def get_aqi_label(aqi):
    labels = {
        1: "Good",
        2: "Fair",
        3: "Moderate",
        4: "Poor",
        5: "Very Poor"
    }
    return labels.get(aqi, "Unknown")


def get_aqi_color(aqi):
    colors = {
        1: "green",
        2: "blue",
        3: "orange",
        4: "red",
        5: "darkred"
    }
    return colors.get(aqi, "gray")


def get_health_advice(aqi):
    if aqi == 1:
        return "Air quality is good. Outdoor activities are safe."
    elif aqi == 2:
        return "Air quality is fair. Most people can continue normal activity."
    elif aqi == 3:
        return "Moderate pollution. Sensitive people should reduce prolonged outdoor activity."
    elif aqi == 4:
        return "Poor air quality. Wear a mask and avoid heavy outdoor exercise."
    else:
        return "Very poor air quality. Avoid outdoor exposure. Children and elderly should remain indoors."


def get_risk_level(aqi):
    levels = {
        1: "🟢 Low Risk",
        2: "🟡 Mild Risk",
        3: "🟠 Moderate Risk",
        4: "🔴 High Risk",
        5: "🚨 Severe Risk"
    }
    return levels.get(aqi, "Unknown")