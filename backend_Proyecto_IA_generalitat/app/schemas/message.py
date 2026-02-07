"""
Message Schemas.

This module defines Pydantic models for message-related requests and responses.
"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Literal

class MessageResponse(BaseModel):
    """
    Schema for message details response.
    
    Attributes:
        id_mensaje (int): The message ID.
        id_chat (int): The chat ID.
        emisor (str): The sender ("USER" or "IA").
        contenido (str): The message content.
        sent_at (datetime): Timestamp when the message was sent.
    """
    id_mensaje: int
    id_chat: int
    emisor: Literal["USER", "IA"]
    contenido: str
    sent_at: datetime

    class Config:
        from_attributes = True

class CreateMessageRequest(BaseModel):
    """
    Schema for creating a new message request.
    
    Attributes:
        contenido (str): The content of the message.
    """
    contenido: str = Field(min_length=1, max_length=8000)
