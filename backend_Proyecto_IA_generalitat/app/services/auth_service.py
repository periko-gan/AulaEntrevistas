"""
Authentication Service.

This module provides business logic for user authentication, including registration and login.
"""

from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.repositories.user_repo import user_repo
from app.core.security import hash_password, verify_password, create_access_token

class AuthService:
    """Service class for handling authentication logic."""

    def register(self, db: Session, email: str, password: str, nombre: str) -> str:
        """
        Register a new user with email and password.
        
        Args:
            db (Session): Database session.
            email (str): User's email.
            password (str): User's password.
            nombre (str): User's name.
            
        Returns:
            str: JWT access token.
            
        Raises:
            HTTPException: If email is already registered.
        """
        if user_repo.get_by_email(db, email):
            raise HTTPException(status_code=409, detail="Email already registered")
        user = user_repo.create(db, email=email, password_hash=hash_password(password), nombre=nombre)
        return create_access_token(str(user.id_usuario))

    def login(self, db: Session, email: str, password: str) -> str:
        """
        Authenticate user with email and password.
        
        Args:
            db (Session): Database session.
            email (str): User's email.
            password (str): User's password.
            
        Returns:
            str: JWT access token.
            
        Raises:
            HTTPException: If credentials are invalid.
        """
        user = user_repo.get_by_email(db, email)
        if not user or not verify_password(password, user.password_hash):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return create_access_token(str(user.id_usuario))

auth_service = AuthService()
