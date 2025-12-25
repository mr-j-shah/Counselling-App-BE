from app.utils.validation import is_valid_email
from app.schemas.auth.signin import SigninRequest, SigninResponse
from app.schemas.user.user import UserResponse
from fastapi import HTTPException, status


def check_valid_user(request: SigninRequest) -> SigninResponse:
    if not is_valid_email(request.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email format"
        )

    if request.email != "jinay@gmail.com" or request.password != "123456":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
        
    access_token = "mock_jwt_token_here"
    user = UserResponse(
        id=1,
        name="Jinay Shah",
        email=request.email
    )

    return SigninResponse(
        access_token=access_token,
        token_type="bearer",
        user=user
    )
