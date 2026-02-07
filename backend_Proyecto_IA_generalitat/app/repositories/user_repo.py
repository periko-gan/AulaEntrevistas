"""
User Repository.

This module provides data access methods for the User model, including creation and retrieval.
"""

from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.user import User

class UserRepo:
    """Repository class for User model operations."""

    def get_by_email(self, db: Session, email: str) -> User | None:
        """
        Retrieve a user by email address.
        
        Args:
            db (Session): Database session.
            email (str): Email address to search for.
            
        Returns:
            User | None: The user object if found, else None.
        """
        return db.scalar(select(User).where(User.email == email))

    def get_by_id(self, db: Session, user_id: int) -> User | None:
        """
        Retrieve a user by ID.
        
        Args:
            db (Session): Database session.
            user_id (int): ID of the user.
            
        Returns:
            User | None: The user object if found, else None.
        """
        return db.get(User, user_id)

    def create(self, db: Session, email: str, password_hash: str, nombre: str) -> User:
        """
        Create a new user in the database.
        
        Args:
            db (Session): Database session.
            email (str): User's email.
            password_hash (str): Hashed password.
            nombre (str): User's name.
            
        Returns:
            User: The newly created user.
        """
        user = User(email=email, password_hash=password_hash, nombre=nombre)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

user_repo = UserRepo()
