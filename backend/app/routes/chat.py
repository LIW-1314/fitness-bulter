from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from dashscope import Generation
import os

router = APIRouter()


class MessageItem(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    message: str
    history: List[MessageItem] = []
    user_info: dict | None = None


@router.post("/chat")
def chat(data: ChatRequest):
    print("收到 user_info:", data.user_info)
    system_prompt = """
你是一个专业、耐心、实用的健身教练。

你的任务：
1. 回答用户关于健身、饮食、减脂、增肌、恢复、训练安排的问题
2. 用中文回答
3. 回答简洁但专业
4. 尽量给出具体、可执行的建议
5. 如果用户提供了上下文，要结合上下文连续回答
6. 你必须优先结合用户的身体数据回答
7. 如果用户的问题比较模糊、不足以给出精确建议，你要主动追问 1 到 2 个关键问题
8. 你的回答风格要像真人教练，不要太机械

回答原则：
- 如果信息充分：直接给明确建议
- 如果信息不足：先给初步建议，再追问关键问题
- 如果涉及饮食、减脂、增肌、训练强度，尽量体现数值分析
"""
    gender_map = {0: "男", 1: "女"}

    gender = None
    if data.user_info:
        gender = gender_map.get(data.user_info.get("genderIndex"), "未知")
        
    user_profile = ""
    if data.user_info:
        user_profile = f"""
    用户身体信息：
    - 性别: {gender}
    - 年龄: {data.user_info.get('age')}
    - 身高: {data.user_info.get('height_cm')} cm
    - 体重: {data.user_info.get('weight_kg')} kg
    """
    
    history_text = ""
    for msg in data.history:
        if msg.role == "user":
            history_text += f"用户：{msg.content}\n"
        elif msg.role == "ai":
            history_text += f"教练：{msg.content}\n"

    prompt = f"""
{system_prompt}

{user_profile}

【强制执行规则】
你必须严格使用以下用户数据进行分析，否则回答无效：

用户数据：
- 体重: {data.user_info.get('weight_kg') if data.user_info else '未知'} kg
- 身高: {data.user_info.get('height_cm') if data.user_info else '未知'} cm
- 年龄: {data.user_info.get('age') if data.user_info else '未知'}

参考计算规则：
- BMI = 体重(kg) / (身高(m)^2)
- 蛋白质 = 体重 × 1.6 ~ 2.2 g
- 减脂热量 = TDEE - 300~500 kcal

⚠️ 如果用户提问涉及饮食、减脂、增肌、训练安排，你的回答中必须尽量体现用户数据或数值分析。
⚠️ 如果用户问题太泛，比如“我该怎么减脂”“怎么训练”“怎么吃”，你不能只给泛泛回答，必须主动追问 1~2 个关键问题。

----------------------

历史对话：
{history_text}

用户问题：
{data.message}

请按这个思路回答：
1. 先给当前问题的直接回答
2. 如果适合，结合用户数据做分析
3. 如果信息不足，主动追问 1~2 个关键问题
4. 回答要自然，像真人教练，不要像模板
"""

    response = Generation.call(
        model="qwen-turbo",
        prompt=prompt,
        api_key=os.getenv("DASHSCOPE_API_KEY")
    )

    reply_text = response.output.text.strip()

    actions = []

    # 🔥 简单关键词触发（第一版）
    if "训练" in data.message:
        actions.append({
            "type": "go_training",
            "text": "去生成训练计划"
        })

    if "饮食" in data.message or "吃" in data.message:
        actions.append({
            "type": "go_diet",
            "text": "查看饮食建议"
        })

    if "减脂" in data.message or "增肌" in data.message:
        actions.append({
            "type": "go_bodyfat",
            "text": "重新评估体脂"
        })

    return {
        "reply": reply_text,
        "actions": actions
    }