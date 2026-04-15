from app.services.ai_service import generate_training_plan_with_ai


def generate_training_plan(goal, experience, days):
    try:
        return generate_training_plan_with_ai(goal, experience, days)
    except Exception as e:
        print("AI 生成失败，回退到规则方案：", e)

        plan = []

        if days == 3:
            plan = [
                {"day": "第1天", "focus": "全身", "advice": "控制节奏"},
                {"day": "第2天", "focus": "上肢", "advice": "注意发力"},
                {"day": "第3天", "focus": "下肢", "advice": "动作标准"}
            ]
        else:
            plan = [
                {"day": "第1天", "focus": "胸", "advice": "卧推主练"},
                {"day": "第2天", "focus": "背", "advice": "背部发力"},
                {"day": "第3天", "focus": "腿", "advice": "重视下肢"}
            ]

        return {
            "plan": plan,
            "extra_advice": ["保持训练节奏", "注意恢复"]
        }