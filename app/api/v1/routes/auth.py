from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.auth import (
    SignUpRequest, LoginRequest, LoginResponse,
    ForgotPasswordRequest, ForgotPasswordResponse,
    ResetPasswordRequest, ResetPasswordResponse,
    VerifyTokenResponse
)
from app.services.auth_service import (
    signup, login, forgot_password, verify_reset_token, reset_password
)

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/signup")
async def signup_api(request: SignUpRequest, db: AsyncSession = Depends(get_db)):
    return await signup(db, request)

@router.post("/login", response_model=LoginResponse)
async def login_api(request: LoginRequest, db: AsyncSession = Depends(get_db)):
    return await login(db, request)

@router.post("/forgot-password", response_model=ForgotPasswordResponse, status_code=200)
async def forgot_password_api(
    request: ForgotPasswordRequest,
    db: AsyncSession = Depends(get_db)
):
    return await forgot_password(db, request)

@router.get("/reset-password/verify", response_model=VerifyTokenResponse)
async def verify_reset_token_api(
    token: str = Query(..., description="Password reset token"),
    db: AsyncSession = Depends(get_db)
):
    try:
        return await verify_reset_token(db, token)
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Invalid or expired token."
        )

@router.post("/reset-password", response_model=ResetPasswordResponse, status_code=200)
async def reset_password_api(
    request: ResetPasswordRequest,
    db: AsyncSession = Depends(get_db)
):
    return await reset_password(db, request)