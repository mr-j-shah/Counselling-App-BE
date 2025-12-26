from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException, status
from app.db.models.user import User
from app.schemas.auth import SignUpRequest, LoginRequest, LoginResponse, UserResponse
from app.core.security import hash_password, verify_password, create_access_token

async def signup(db: AsyncSession, request: SignUpRequest):
    result = await db.execute(select(User).where(User.email == request.email))
    existing_user = result.scalar_one_or_none()
    
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    user = User(
        name=request.name,
        email=request.email,
        hashed_password=hash_password(request.password)
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return {"message": "Signup successful"}

async def login(db: AsyncSession, request: LoginRequest) -> LoginResponse:
    result = await db.execute(select(User).where(User.email == request.email))
    user = result.scalar_one_or_none()
    
    if not user or not verify_password(request.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_access_token({"sub": str(user.id)})
    return LoginResponse(
        access_token=token,
        user=UserResponse(
            id=user.id,
            name=user.name,
            email=user.email
        )
    )
