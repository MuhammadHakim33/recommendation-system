from fastapi import APIRouter
from services.recommendation_service import get_user_vector

router = APIRouter()

@router.get("/recommendation/{user_id}")
def get_recommendation(user_id: int):
    return get_user_vector(user_id)