"""
Message Repository.

This module provides data access methods for the Message model, including creation and retrieval.
"""

from sqlalchemy.orm import Session
from sqlalchemy import select, func
from app.models.message import Message
from app.models.chat import Chat

class MessageRepo:
    """Repository class for Message model operations."""

    def list_for_chat(self, db: Session, chat_id: int, limit: int = 50) -> list[Message]:
        """
        Retrieve messages for a chat in descending order by timestamp.
        
        Args:
            db (Session): Database session.
            chat_id (int): ID of the chat.
            limit (int): Maximum number of messages to retrieve.
            
        Returns:
            list[Message]: List of messages in the chat.
        """
        stmt = select(Message).where(Message.id_chat == chat_id).order_by(Message.sent_at.desc()).limit(limit)
        return list(db.scalars(stmt))

    def create(self, db: Session, chat_id: int, emisor: str, contenido: str) -> Message:
        """
        Create a new message and update the chat's last_message_at timestamp.
        
        Args:
            db (Session): Database session.
            chat_id (int): ID of the chat.
            emisor (str): Sender of the message ("USER" or "IA").
            contenido (str): Content of the message.
            
        Returns:
            Message: The newly created message.
        """
        msg = Message(id_chat=chat_id, emisor=emisor, contenido=contenido)
        db.add(msg)

        chat = db.get(Chat, chat_id)
        if chat:
            chat.last_message_at = func.now()

        db.commit()
        db.refresh(msg)
        return msg

message_repo = MessageRepo()
