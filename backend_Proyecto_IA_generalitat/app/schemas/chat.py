"""
Chat Schemas.

This module defines Pydantic models for chat-related requests and responses,
including chat creation, updates, and retrieval.
"""

from pydantic import BaseModel, Field, field_validator
from datetime import datetime


class ChatResponse(BaseModel):
    """
    Schema for chat details response.
    
    Attributes:
        id_chat (int): The chat ID.
        id_usuario (int): The ID of the user who owns the chat.
        title (str): The chat title.
        status (str): The chat status ('active' or 'completed').
        created_at (datetime): Creation timestamp.
        last_message_at (datetime | None): Timestamp of the last message.
        completed_at (datetime | None): Completion timestamp.
    """
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
    """
    Schema for chat creation response.
    
    Attributes:
        id_chat (int): The ID of the newly created chat.
    """
    id_chat: int


class UpdateChatTitleRequest(BaseModel):
    """
    Schema for updating chat title request.
    
    Attributes:
        title (str): The new title for the chat.
    """
    title: str = Field(..., min_length=1, max_length=200, description="Título del chat")
    
    @field_validator('title')
    @classmethod
    def validate_title(cls, v: str) -> str:
        """Valida y limpia el título."""
        cleaned = v.strip()
        if not cleaned:
            raise ValueError('El título no puede estar vacío')
        return cleaned


class UpdateChatStatusRequest(BaseModel):
    """
    Schema for updating chat status request.
    
    Attributes:
        status (str): The new status ('active' or 'completed').
    """
    status: str = Field(..., description="Nuevo estado del chat: 'active' o 'completed'")
    
    @field_validator('status')
    @classmethod
    def validate_status(cls, v: str) -> str:
        """Valida que el estado sea válido."""
        if v not in ['active', 'completed']:
            raise ValueError("El estado debe ser 'active' o 'completed'")
        return v
