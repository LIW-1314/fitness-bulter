import os
import json
from dashscope import Generation
from dotenv import load_dotenv
import os
import json
load_dotenv()

DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY")


def generate_training_plan_with_ai(goal: str, experience: str, days_per_week: int):
    prompt = f"""
你是一名专业健身教练，擅长为普通健身用户制定详细、可执行、清晰的每周训练计划。

用户信息：
- 目标: {goal}
- 训练经验: {experience}
- 每周训练天数: {days_per_week}

请你根据用户目标、经验和训练频率，生成一份详细的每周训练计划。

【输出要求】
你必须严格返回合法 JSON，不允许输出任何解释、前言、说明、markdown代码块或多余文字。

返回 JSON 格式必须如下：
{{
  "plan": [
    {{
      "day": "第1天",
      "focus": "胸部 + 三头",
      "summary": "一句话概括当天训练思路",
      "muscle_groups": ["胸大肌", "肱三头肌"],
      "exercises": [
        {{
          "name": "平板卧推",
          "target": "胸部",
          "sets": 4,
          "reps": "6-10次",
          "rest": "90秒"
        }},
        {{
          "name": "上斜哑铃卧推",
          "target": "胸部上沿",
          "sets": 3,
          "reps": "8-12次",
          "rest": "60-90秒"
        }}
      ],
      "advice": "当天训练注意事项"
    }}
  ],
  "extra_advice": [
    "建议1",
    "建议2",
    "建议3"
  ]
}}

【硬性规则】
1. 只能返回 JSON
2. 所有内容必须用中文
3. plan 的数量必须严格等于每周训练天数 {days_per_week}
4. 每一天都必须包含：
   - day
   - focus
   - summary
   - muscle_groups
   - exercises
   - advice
5. 每一天的 exercises 必须包含 4 到 6 个推荐动作
6. 每个动作必须包含：
   - name
   - target
   - sets
   - reps
   - rest
7. 动作名称要具体，不要只写“胸部训练”“背部训练”这种模糊词
8. 训练计划要适合普通健身房场景，优先选择常见器械和自由重量动作
9. 必须考虑训练经验：
   - 如果是 beginner，新手动作优先、动作数量适中、强度不要过高
   - 如果是 intermediate，动作可以更丰富，训练容量可以略高
10. 必须考虑训练目标：
   - 如果目标是 fat_loss，计划中可以适当加入有氧或训练密度建议
   - 如果目标是 muscle_gain，优先安排力量训练和渐进超负荷思路
   - 如果目标是 maintain，计划以均衡和可持续为主
11. 每天训练的部位安排要合理，避免连续两天高强度重复同一肌群
12. extra_advice 至少包含 3 条，内容要具体实用

【训练编排要求】
- 3天训练：优先考虑推/拉/腿，或者全身/上肢/下肢
- 4天训练：优先考虑上/下肢拆分，或推/拉/腿/补弱项
- 5天训练：可以采用胸、背、腿、肩、手臂/核心的拆分
- 6天训练：可以采用更细致的部位拆分，但仍要注意恢复
- 每天先安排复合动作，再安排孤立动作
- 动作顺序要有逻辑，不要混乱堆砌

【动作风格要求】
- 优先推荐经典、常见、可执行的动作，例如：
  平板卧推、上斜哑铃卧推、高位下拉、坐姿划船、深蹲、腿举、罗马尼亚硬拉、肩推、侧平举、绳索下压、哑铃弯举等
- 不要给过于冷门、风险过高、花哨但不实用的动作
- 不要只给部位，不给动作

现在请直接输出符合要求的 JSON。
"""

    response = Generation.call(
        model="qwen-turbo",
        prompt=prompt,
        api_key=DASHSCOPE_API_KEY
    )

    text = response.output.text.strip()

    try:
        return json.loads(text)
    except:
        print("解析失败，原始输出：", text)
        raise Exception("AI返回格式错误")

def generate_diet_advice_with_ai(data):
    prompt = f"""
你是一个专业健身营养师，擅长为普通健身用户制定具体、可执行的饮食建议。

用户数据：
- 性别: {data['gender']}
- 年龄: {data['age']}
- 身高: {data['height_cm']} cm
- 体重: {data['weight_kg']} kg
- 目标: {data['goal']}

营养目标：
- 每日热量: {data['target_calories']} kcal
- 蛋白质: {data['protein_g']} g
- 脂肪: {data['fat_g']} g
- 碳水: {data['carb_g']} g

请基于这些信息，生成一个详细、易执行的饮食建议。

【输出要求】
你必须严格返回合法 JSON，不允许输出任何解释、前言、markdown代码块或多余文字。

返回 JSON 格式必须如下：
{{
  "diet_strategy": "一句话概括整体饮食策略",
  "advice": [
    "建议1",
    "建议2",
    "建议3"
  ],
  "meal_plan": {{
    "breakfast": [
      "食物1",
      "食物2"
    ],
    "lunch": [
      "食物1",
      "食物2"
    ],
    "dinner": [
      "食物1",
      "食物2"
    ],
    "snack": [
      "食物1",
      "食物2"
    ]
  }}
}}

【硬性规则】
1. 只能返回 JSON
2. 所有内容必须用中文
3. advice 至少返回 3 条，最多 5 条
4. 必须返回 meal_plan，且包含 breakfast、lunch、dinner、snack 四个字段
5. 每一餐至少给 2~4 个具体食物，不要空泛描述
6. 食物要适合普通人日常生活，易获取、易执行
7. 必须结合用户目标：
   - 如果 goal 是 fat_loss：更强调控热量、优质蛋白、饱腹感
   - 如果 goal 是 muscle_gain：更强调热量盈余、蛋白质和碳水补充
   - 如果 goal 是 maintain：更强调均衡和长期可持续
8. 不要只写“高蛋白食物”“优质碳水”这种抽象词，必须写具体食物，比如鸡蛋、燕麦、鸡胸肉、米饭、牛奶、香蕉等
9. diet_strategy 要简洁清晰，像营养师总结
"""

    from dashscope import Generation
    import os
    import json

    response = Generation.call(
        model="qwen-turbo",
        prompt=prompt,
        api_key=os.getenv("DASHSCOPE_API_KEY")
    )

    text = response.output.text.strip()

    try:
        return json.loads(text)
    except:
        print("AI饮食解析失败:", text)
        return {
            "diet_strategy": "建议优先保证蛋白质摄入，并保持饮食均衡。",
            "advice": ["饮食建议生成失败，请稍后重试"],
            "meal_plan": {
                "breakfast": ["鸡蛋", "燕麦", "牛奶"],
                "lunch": ["米饭", "鸡胸肉", "蔬菜"],
                "dinner": ["土豆", "牛肉", "蔬菜"],
                "snack": ["酸奶", "香蕉"]
            }
        }
        
def generate_today_advice_with_ai(data):
    prompt = f"""
    你是一个专业健身教练和健康顾问。

    用户信息：
    - 健身目标: {data['goal']}
    - 今日训练类型: {data['training']}

    天气信息：
    - 当前温度: {data['temperature']} °C
    - 体感温度: {data['apparent_temperature']} °C
    - 最高温: {data['temp_max']} °C
    - 最低温: {data['temp_min']} °C
    - 降水: {data['precipitation_sum']} mm
    - 风速: {data['wind_speed']} km/h

    请结合天气和训练安排，生成今天的健身建议。

    要求：
    1. 用中文
    2. 返回 3 到 5 条建议
    3. 建议要具体、实用
    4. 不要空话
    5. 只返回 JSON，不要任何解释

    返回格式：
    {{
    "advice": [
        "建议1",
        "建议2",
        "建议3"
    ]
    }}
"""



    response = Generation.call(
        model="qwen-turbo",
        prompt=prompt,
        api_key=os.getenv("DASHSCOPE_API_KEY")
    )

    text = response.output.text.strip()

    try:
        return json.loads(text)
    except:
        print("AI 今日建议解析失败:", text)
        return {
            "advice": ["今日建议生成失败，请稍后重试"]
        }