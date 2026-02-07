"""
User Schemas.

This module defines Pydantic models for user-related responses.
"""

from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserResponse(BaseModel):
    """
    Schema for user profile response.
    
    Attributes:
        id_usuario (int): The user ID.
        email (EmailStr): The user's email address.
        nombre (str): The user's full name.
        created_at (datetime): Registration timestamp.
    """
    id_usuario: int
    email: EmailStr
    nombre: str
    created_at: datetime

    class Config:
        from_attributes = True
