from fastapi import APIRouter
from pydantic import BaseModel
from app.services.training_service import generate_training_plan

router = APIRouter()


class TrainingRequest(BaseModel):
    goal: str
    experience: str
    days_per_week: int


@router.post("/plan")
def get_plan(data: TrainingRequest):
    return generate_training_plan(
        data.goal,
        data.experience,
        data.days_per_week
    )