from fastapi import APIRouter, HTTPException
from src.models.user_model import Token, TokenResponse, UserCreate, UserLogin, UserOut
from src.services.user_service import authenticate_user, create_user

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=UserOut)
def register_user(user: UserCreate):
    try:
        return create_user(user)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login", response_model=TokenResponse)
def login(credentials: UserLogin):
    token_user = authenticate_user(credentials.username, credentials.password)
    if not token_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token, user_dict = token_user
    user_dict.pop("password", None)

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": user_dict
    }