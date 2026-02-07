"""
User Model.

This module defines the User database model, representing a registered user of the application.
"""

from sqlalchemy import String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

class User(Base):
    """
    User database model.
    
    Attributes:
        id_usuario (int): Primary key.
        email (str): User's email address (unique).
        password_hash (str): Hashed password.
        nombre (str): User's full name.
        created_at (datetime): Timestamp when the user was created.
        chats (list[Chat]): Relationship to the Chat model.
    """
    __tablename__ = "users"

    id_usuario: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    nombre: Mapped[str] = mapped_column(String(120), nullable=False)
    created_at: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=func.now())

    chats = relationship("Chat", back_populates="user", cascade="all, delete-orphan")
