"""
Message Service.

This module provides business logic for managing messages, including creation, retrieval,
and formatting for AI services.
"""

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.message_repo import message_repo
from app.services.chat_service import chat_service
from app.models.message import Message


class MessageService:
    """Service class for handling message-related logic."""

    def list_messages(self, db: Session, chat_id: int, user_id: int, limit: int = 50) -> list[Message]:
        """
        Retrieve messages for a chat (validates ownership).
        
        Args:
            db (Session): Database session.
            chat_id (int): ID of the chat.
            user_id (int): ID of the user.
            limit (int): Maximum number of messages to retrieve.
            
        Returns:
            list[Message]: List of messages in the chat.
        """
        chat_service.get_chat_for_user_or_404(db, chat_id, user_id)
        return message_repo.list_for_chat(db, chat_id, limit=limit)

    def create_user_message(self, db: Session, chat_id: int, user_id: int, contenido: str) -> Message:
        """
        Create a user message (validates chat ownership and content).
        
        Args:
            db (Session): Database session.
            chat_id (int): ID of the chat.
            user_id (int): ID of the user.
            contenido (str): Content of the message.
            
        Returns:
            Message: The created message object.
            
        Raises:
            HTTPException: If content is empty.
        """
        if not contenido or not contenido.strip():
            raise HTTPException(status_code=422, detail="Message content cannot be empty")

        chat_service.get_chat_for_user_or_404(db, chat_id, user_id)
        return message_repo.create(db, chat_id, "USER", contenido.strip())

    def create_ai_message(self, db: Session, chat_id: int, user_id: int, contenido: str) -> Message:
        """
        Create an AI message (validates chat ownership and content).
        
        Args:
            db (Session): Database session.
            chat_id (int): ID of the chat.
            user_id (int): ID of the user.
            contenido (str): Content of the message.
            
        Returns:
            Message: The created message object.
            
        Raises:
            HTTPException: If content is empty.
        """
        if not contenido or not contenido.strip():
            raise HTTPException(status_code=500, detail="AI response was empty")

        chat_service.get_chat_for_user_or_404(db, chat_id, user_id)
        return message_repo.create(db, chat_id, "IA", contenido.strip())

    def build_bedrock_history(self, db: Session, chat_id: int, user_id: int, limit: int = 50) -> list[dict]:
        """
        Build Bedrock API message history in [{"role": "user"|"assistant", "content": "..."}] format (chronological order).
        
        Args:
            db (Session): Database session.
            chat_id (int): ID of the chat.
            user_id (int): ID of the user.
            limit (int): Maximum number of messages to include in history.
            
        Returns:
            list[dict]: List of message dictionaries formatted for Bedrock.
        """
        chat_service.get_chat_for_user_or_404(db, chat_id, user_id)
        msgs = message_repo.list_for_chat(db, chat_id, limit=limit)
        msgs = list(reversed(msgs))

        history: list[dict] = []
        for m in msgs:
            role = "user" if m.emisor == "USER" else "assistant"
            history.append({"role": role, "content": m.contenido})
        return history


message_service = MessageService()
