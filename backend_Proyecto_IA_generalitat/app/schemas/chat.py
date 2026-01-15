from pydantic import BaseModel, Field, field_validator
from datetime import datetime


class ChatResponse(BaseModel):
    id_chat: int
    id_usuario: int
    title: str
    status: str
    created_at: datetime
    last_message_at: datetime | None
    completed_at: datetime | None

    class Config:
        from_attributes = True


class CreateChatResponse(BaseModel):
    id_chat: int


class UpdateChatTitleRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=200, description="Título del chat")
    
    @field_validator('title')
    @classmethod
    def validate_title(cls, v: str) -> str:
        """Valida y limpia el título."""
        cleaned = v.strip()
        if not cleaned:
            raise ValueError('El título no puede estar vacío')
        return cleaned
