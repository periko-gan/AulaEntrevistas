"""
Chat Model.

This module defines the Chat database model, representing a conversation between a user and the AI.
"""

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from datetime import datetime

class Chat(Base):
    """
    Chat database model.
    
    Attributes:
        id_chat (int): Primary key.
        id_usuario (int): Foreign key to the user who owns the chat.
        title (str): Title of the chat session.
        status (str): Current status of the chat ('active' or 'completed').
        created_at (datetime): Timestamp when the chat was created.
        last_message_at (datetime): Timestamp of the last message in the chat.
        completed_at (datetime): Timestamp when the chat was marked as completed.
        user (User): Relationship to the User model.
        mensajes (list[Message]): Relationship to the Message model.
    """
    __tablename__ = "chats"

    id_chat: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    id_usuario: Mapped[int] = mapped_column(ForeignKey("users.id_usuario"), nullable=False, index=True)
    title: Mapped[str | None] = mapped_column(nullable=False, default="Nuevo Chat")
    status: Mapped[str] = mapped_column(String(20), default="active", nullable=False)  # 'active' | 'completed'
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    last_message_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    user = relationship("User", back_populates="chats")
    mensajes = relationship("Message", back_populates="chat", cascade="all, delete-orphan")
