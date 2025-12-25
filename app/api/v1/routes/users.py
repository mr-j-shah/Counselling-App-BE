from fastapi import APIRouter
from app.schemas.user.user import UserCreate, UserResponse
from app.schemas.base import BaseResponse
from app.services.user_service import create_user

router = APIRouter(prefix="/users")

@router.post("/", response_model=BaseResponse[UserResponse])
def create(user: UserCreate):
    return BaseResponse(
        success=True,
        message="User fetched successfully",
        data=create_user(user)
    )
