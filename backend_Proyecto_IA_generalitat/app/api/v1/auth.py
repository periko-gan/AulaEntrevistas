from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.auth import RegisterRequest, LoginRequest, TokenResponse
from app.schemas.user import UserResponse
from app.services.auth_service import auth_service
from app.api.deps import get_current_user

router = APIRouter()

@router.post("/register", response_model=TokenResponse)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    """Register a new user and return access token."""
    token = auth_service.register(db, payload.email, payload.password, payload.nombre)
    return TokenResponse(access_token=token)

@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    """Authenticate a user and return access token."""
    token = auth_service.login(db, payload.email, payload.password)
    return TokenResponse(access_token=token)

@router.get("/me", response_model=UserResponse)
def get_current_user_info(user=Depends(get_current_user)):
    """Retrieve the authenticated user's profile."""
    return user
