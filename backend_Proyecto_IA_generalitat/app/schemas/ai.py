"""
AI Schemas.

This module defines Pydantic models for AI-related requests, such as generating replies,
initializing chats, and generating reports.
"""

from pydantic import BaseModel, Field

class AiReplyRequest(BaseModel):
    """
    Schema for a request to generate an AI reply.
    
    Attributes:
        chat_id (int): The ID of the chat.
        contenido (str): The content of the user's message.
    """
    chat_id: int = Field(..., ge=1)
    contenido: str = Field(..., min_length=1, max_length=8000)

class InitializeChatRequest(BaseModel):
    """
    Schema for a request to initialize a chat with an AI greeting.
    
    Attributes:
        chat_id (int): The ID of the chat to initialize.
    """
    chat_id: int = Field(..., ge=1)

class GenerateReportRequest(BaseModel):
    """
    Schema for a request to generate an interview report.
    
    Attributes:
        chat_id (int): The ID of the chat to generate a report for.
    """
    chat_id: int = Field(..., ge=1)
