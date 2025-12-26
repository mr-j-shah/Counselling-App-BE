from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.auth import SignUpRequest, LoginRequest, LoginResponse
from app.services.auth_service import signup, login

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/signup")
async def signup_api(request: SignUpRequest, db: AsyncSession = Depends(get_db)):
    return await signup(db, request)

@router.post("/login", response_model=LoginResponse)
async def login_api(request: LoginRequest, db: AsyncSession = Depends(get_db)):
    return await login(db, request)

