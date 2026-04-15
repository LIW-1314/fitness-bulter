from app.services.weather_service import get_weather_by_location
from app.services.ai_service import generate_today_advice_with_ai


def generate_today_advice(latitude, longitude, goal, training):
    weather = get_weather_by_location(latitude, longitude)

    try:
        ai_result = generate_today_advice_with_ai({
            "goal": goal,
            "training": training,
            "temperature": weather.get("temperature"),
            "apparent_temperature": weather.get("apparent_temperature"),
            "temp_max": weather.get("temp_max"),
            "temp_min": weather.get("temp_min"),
            "precipitation_sum": weather.get("precipitation_sum"),
            "wind_speed": weather.get("wind_speed")
        })

        advice = ai_result.get("advice", [])
    except Exception as e:
        print("AI 今日建议失败，回退到规则方案：", e)

        advice = []
        temp = weather.get("temperature")

        if temp is not None:
            if temp > 30:
                advice.append("天气较热，建议避免中午训练，优先选择早晚时段。")
            elif temp < 10:
                advice.append("天气较冷，训练前注意充分热身。")

        if training == "cardio":
            advice.append("今天如进行有氧，建议控制在30到45分钟。")
        elif training == "strength":
            advice.append("今天如进行力量训练，注意训练节奏和补水。")

        advice.append("请根据自身状态灵活调整训练强度。")

    return {
        "weather": weather,
        "advice": advice
    }