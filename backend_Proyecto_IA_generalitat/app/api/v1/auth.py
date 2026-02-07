"""
Authentication API endpoints.

This module provides endpoints for user registration, login, and retrieving
current user information.
"""

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
    """
    Register a new user and return access token.

    Args:
        payload (RegisterRequest): The registration data (email, password, name).
        db (Session): The database session.

    Returns:
        TokenResponse: The access token for the newly registered user.
    """
    token = auth_service.register(db, payload.email, payload.password, payload.nombre)
    return TokenResponse(access_token=token)

@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    """
    Authenticate a user and return access token.

    Args:
        payload (LoginRequest): The login credentials (email, password).
        db (Session): The database session.

    Returns:
        TokenResponse: The access token for the authenticated user.
    """
    token = auth_service.login(db, payload.email, payload.password)
    return TokenResponse(access_token=token)

@router.get("/me", response_model=UserResponse)
def get_current_user_info(user=Depends(get_current_user)):
    """
    Retrieve the authenticated user's profile.

    Args:
        user (User): The currently authenticated user (injected via dependency).

    Returns:
        UserResponse: The user's profile information.
    """
    return user
