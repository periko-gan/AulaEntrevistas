from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserResponse(BaseModel):
    id_usuario: int
    email: EmailStr
    nombre: str
    created_at: datetime

    class Config:
        from_attributes = True
