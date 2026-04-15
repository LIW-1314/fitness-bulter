from fastapi import APIRouter
from pydantic import BaseModel
from app.services.bodyfat_service import calculate_bodyfat_result

router = APIRouter()


class BodyFatRequest(BaseModel):
    gender: str
    age: int
    height_cm: float
    weight_kg: float


@router.post("/calculate")
def calculate_bodyfat(data: BodyFatRequest):
    return calculate_bodyfat_result(
        gender=data.gender,
        age=data.age,
        height_cm=data.height_cm,
        weight_kg=data.weight_kg
    )