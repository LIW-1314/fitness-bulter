def calculate_bodyfat_result(gender: str, age: int, height_cm: float, weight_kg: float):
    height_m = height_cm / 100
    bmi = weight_kg / (height_m ** 2)

    if gender == "male":
        body_fat = 1.2 * bmi + 0.23 * age - 16.2
    else:
        body_fat = 1.2 * bmi + 0.23 * age - 5.4

    body_fat = round(body_fat, 1)

    if gender == "male":
        if body_fat < 6:
            level = "偏低"
        elif body_fat < 14:
            level = "精瘦"
        elif body_fat < 18:
            level = "标准"
        elif body_fat < 25:
            level = "偏高"
        else:
            level = "肥胖风险较高"
    else:
        if body_fat < 14:
            level = "偏低"
        elif body_fat < 21:
            level = "精瘦"
        elif body_fat < 25:
            level = "标准"
        elif body_fat < 32:
            level = "偏高"
        else:
            level = "肥胖风险较高"

    return {
        "bmi": round(bmi, 1),
        "body_fat": body_fat,
        "level": level
    }