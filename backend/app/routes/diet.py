from fastapi import APIRouter
from pydantic import BaseModel
from app.services.diet_service import generate_diet_plan

router = APIRouter()


class DietRequest(BaseModel):
    gender: str
    age: int
    height_cm: float
    weight_kg: float
    goal: str
    activity_level: str


@router.post("/recommend")
def recommend_diet(data: DietRequest):
    return generate_diet_plan(
        data.gender,
        data.age,
        data.height_cm,
        data.weight_kg,
        data.goal,
        data.activity_level
    )