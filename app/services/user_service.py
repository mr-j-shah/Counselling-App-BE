from app.schemas.user.user import UserResponse
from app.schemas.user.user import UserCreate

def create_user(user_data :UserCreate):
    return UserResponse(id=1,name=user_data.name,email=user_data.email)

