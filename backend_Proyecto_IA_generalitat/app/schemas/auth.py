"""
Authentication Schemas.

This module defines Pydantic models for authentication-related requests and responses,
including registration, login, and token handling.
"""

from pydantic import BaseModel, EmailStr, Field, field_validator
import re


class RegisterRequest(BaseModel):
    """
    Schema for user registration request.
    
    Attributes:
        email (EmailStr): The user's email address.
        password (str): The user's password (8-128 chars).
        nombre (str): The user's full name (2-120 chars).
    """
    email: EmailStr  # Ya valida formato
    password: str = Field(min_length=8, max_length=128, description="Contraseña entre 8-128 caracteres")
    nombre: str = Field(min_length=2, max_length=120, description="Nombre del usuario")
    
    @field_validator('nombre')
    @classmethod
    def validate_nombre(cls, v: str) -> str:
        """Valida que el nombre solo contenga letras y espacios."""
        if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', v):
            raise ValueError('El nombre solo puede contener letras y espacios')
        return v.strip()
    
    @field_validator('password')
    @classmethod
    def validate_password(cls, v: str) -> str:
        """Valida fortaleza mínima de contraseña."""
        if not any(c.isdigit() for c in v):
            raise ValueError('La contraseña debe contener al menos un número')
        if not any(c.isalpha() for c in v):
            raise ValueError('La contraseña debe contener al menos una letra')
        return v


class LoginRequest(BaseModel):
    """
    Schema for user login request.
    
    Attributes:
        email (EmailStr): The user's email address.
        password (str): The user's password.
    """
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    """
    Schema for authentication token response.
    
    Attributes:
        access_token (str): The JWT access token.
        token_type (str): The type of token (default: "bearer").
    """
    access_token: str
    token_type: str = "bearer"
