from fastapi import APIRouter
from pydantic import BaseModel
from app.services.advice_service import generate_today_advice

router = APIRouter()


class AdviceRequest(BaseModel):
    latitude: float
    longitude: float
    training_goal: str
    planned_training: str


@router.post("/today")
def today(data: AdviceRequest):
    return generate_today_advice(
        data.latitude,
        data.longitude,
        data.training_goal,
        data.planned_training
    )