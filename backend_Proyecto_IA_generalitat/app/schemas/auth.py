from pydantic import BaseModel, EmailStr, Field, field_validator
import re


class RegisterRequest(BaseModel):
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
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
