from fastapi import APIRouter
from app.schemas.auth.signin import SigninRequest, SigninResponse
from app.schemas.user.user import UserResponse
from app.services.auth_service import check_valid_user


router = APIRouter(prefix="/auth")

@router.post("/", response_model=SigninResponse)
def create(user: SigninRequest):
    return check_valid_user(request=user)
