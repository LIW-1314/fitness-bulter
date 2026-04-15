from app.services.ai_service import generate_diet_advice_with_ai


def generate_diet_plan(gender, age, height_cm, weight_kg, goal, activity_level):
    if gender == "male":
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age + 5
    else:
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age - 161

    activity_map = {
        "low": 1.2,
        "medium": 1.55,
        "high": 1.725
    }

    tdee = bmr * activity_map.get(activity_level, 1.2)

    if goal == "fat_loss":
        target_calories = tdee - 400
    elif goal == "muscle_gain":
        target_calories = tdee + 300
    else:
        target_calories = tdee

    protein = weight_kg * 2
    fat = weight_kg * 0.8
    carbs = (target_calories - protein * 4 - fat * 9) / 4

    result = {
        "bmr": round(bmr),
        "tdee": round(tdee),
        "target_calories": round(target_calories),
        "protein_g": round(protein),
        "fat_g": round(fat),
        "carb_g": round(max(carbs, 0))
    }

    try:
        ai_result = generate_diet_advice_with_ai({
            "gender": gender,
            "age": age,
            "height_cm": height_cm,
            "weight_kg": weight_kg,
            "goal": goal,
            **result
        })

        result["diet_strategy"] = ai_result.get("diet_strategy", "")
        result["advice"] = ai_result.get("advice", [])
        result["meal_plan"] = ai_result.get("meal_plan", {
            "breakfast": [],
            "lunch": [],
            "dinner": [],
            "snack": []
        })
    except Exception as e:
        print("AI饮食失败:", e)
        result["diet_strategy"] = "建议保持均衡饮食，多摄入优质蛋白。"
        result["advice"] = ["建议保持均衡饮食，多摄入优质蛋白"]
        result["meal_plan"] = {
            "breakfast": ["鸡蛋", "燕麦", "牛奶"],
            "lunch": ["米饭", "鸡胸肉", "蔬菜"],
            "dinner": ["土豆", "牛肉", "蔬菜"],
            "snack": ["酸奶", "香蕉"]
        }

    return result