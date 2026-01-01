from pydantic import BaseModel, EmailStr, Field

class SignUpRequest(BaseModel):
    name: str
    email: EmailStr
    password: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class ForgotPasswordResponse(BaseModel):
    message: str = "If the email exists, a password reset link has been sent."

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str = Field(..., min_length=8, max_length=72)

class ResetPasswordResponse(BaseModel):
    message: str = "Password has been reset successfully."

class VerifyTokenResponse(BaseModel):
    valid: bool
    message: str