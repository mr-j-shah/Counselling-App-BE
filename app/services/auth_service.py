from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException, status
from app.db.models.user import User
from app.db.models.password_reset_token import PasswordResetToken
from app.schemas.auth import (
    SignUpRequest, LoginRequest, LoginResponse, UserResponse,
    ForgotPasswordRequest, ResetPasswordRequest
)
from app.core.security import (
    hash_password, verify_password, create_access_token,
    generate_reset_token, hash_token, verify_token,
    PASSWORD_RESET_TOKEN_EXPIRE_MINUTES
)
from app.utils.email import send_password_reset_email

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

    if not user.isEmailVerified:
        raise HTTPException(status_code=403, detail="Email not verified. Please verify your email.")
    
    token = create_access_token({"sub": str(user.id)})
    return LoginResponse(
        access_token=token,
        user=UserResponse(
            id=user.id,
            name=user.name,
            email=user.email
        )
    )

async def forgot_password(db: AsyncSession, request: ForgotPasswordRequest) -> dict:
    result = await db.execute(select(User).where(User.email == request.email))
    user = result.scalar_one_or_none()
    
    if user:
        reset_token = generate_reset_token()
        token_hash = hash_token(reset_token)
        expires_at = datetime.utcnow() + timedelta(minutes=PASSWORD_RESET_TOKEN_EXPIRE_MINUTES)
        reset_token_record = PasswordResetToken(
            user_id=user.id,
            token_hash=token_hash,
            expires_at=expires_at,
            created_at=datetime.utcnow()
        )
        db.add(reset_token_record)
        await db.commit()
        await send_password_reset_email(user.email, reset_token)
    
    # Always return same response regardless of whether user exists
    return {"message": "If the email exists, a password reset link has been sent."}

async def verify_reset_token(db: AsyncSession, token: str) -> dict:
    """
    Verify if a reset token is valid.
    Returns 200 if valid, raises 400 if invalid/expired/used.
    """
    # Get all active tokens (not expired, not used)
    result = await db.execute(
        select(PasswordResetToken).where(
            PasswordResetToken.used_at.is_(None),
            PasswordResetToken.expires_at > datetime.utcnow()
        )
    )
    tokens = result.scalars().all()
    
    # Check each token hash
    for token_record in tokens:
        if verify_token(token, token_record.token_hash):
            return {
                "valid": True,
                "message": "Token is valid."
            }
    
    # Token not found or invalid
    raise HTTPException(
        status_code=400,
        detail="Invalid or expired token."
    )

async def reset_password(db: AsyncSession, request: ResetPasswordRequest) -> dict:
    """
    Reset password using a valid reset token.
    """
    # Validate password length (bcrypt supports 8-72 chars)
    if len(request.new_password) < 8 or len(request.new_password) > 72:
        raise HTTPException(
            status_code=400,
            detail="Password must be between 8 and 72 characters."
        )
    
    # Get all active tokens
    result = await db.execute(
        select(PasswordResetToken).where(
            PasswordResetToken.used_at.is_(None),
            PasswordResetToken.expires_at > datetime.utcnow()
        )
    )
    tokens = result.scalars().all()
    
    # Find matching token
    token_record = None
    for t in tokens:
        if verify_token(request.token, t.token_hash):
            token_record = t
            break
    
    if not token_record:
        raise HTTPException(
            status_code=400,
            detail="Invalid or expired token."
        )
    
    # Get user
    user_result = await db.execute(select(User).where(User.id == token_record.user_id))
    user = user_result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=400,
            detail="User not found."
        )
    
    # Update password
    user.hashed_password = hash_password(request.new_password)
    
    # Mark token as used
    token_record.used_at = datetime.utcnow()
    
    await db.commit()
    
    return {"message": "Password has been reset successfully."}

