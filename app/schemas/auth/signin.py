from pydantic import BaseModel
from app.schemas.user.user import UserResponse

class SigninRequest(BaseModel):
    email:str
    password:str
    
class SigninResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse