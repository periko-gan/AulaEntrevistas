"""
Chat Repository.

This module provides data access methods for the Chat model, including creation,
retrieval, updating, and deletion.
"""

from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.chat import Chat

class ChatRepo:
    """Repository class for Chat model operations."""

    def create(self, db: Session, user_id: int) -> Chat:
        """
        Create a new chat for a user.
        
        Args:
            db (Session): Database session.
            user_id (int): ID of the user.
            
        Returns:
            Chat: The newly created chat.
        """
        chat = Chat(id_usuario=user_id)
        db.add(chat)
        db.commit()
        db.refresh(chat)
        return chat

    def list_for_user(self, db: Session, user_id: int) -> list[Chat]:
        """
        Retrieve all chats for a user, ordered by most recent first.
        
        Args:
            db (Session): Database session.
            user_id (int): ID of the user.
            
        Returns:
            list[Chat]: List of chats belonging to the user.
        """
        return list(db.scalars(select(Chat).where(Chat.id_usuario == user_id).order_by(Chat.created_at.desc())))

    def get_for_user(self, db: Session, chat_id: int, user_id: int) -> Chat | None:
        """
        Retrieve a specific chat if it belongs to the user.
        
        Args:
            db (Session): Database session.
            chat_id (int): ID of the chat.
            user_id (int): ID of the user.
            
        Returns:
            Chat | None: The chat object if found, else None.
        """
        return db.scalar(select(Chat).where(Chat.id_chat == chat_id, Chat.id_usuario == user_id))

    def delete(self, db: Session, chat_id: int) -> None:
        """
        Delete a chat and all its messages (cascade).
        
        Args:
            db (Session): Database session.
            chat_id (int): ID of the chat to delete.
        """
        chat = db.get(Chat, chat_id)
        if chat:
            db.delete(chat)
            db.commit()

    def update_title(self, db: Session, chat_id: int, title: str) -> Chat | None:
        """
        Update the title of a chat.
        
        Args:
            db (Session): Database session.
            chat_id (int): ID of the chat.
            title (str): New title.
            
        Returns:
            Chat | None: The updated chat object if found, else None.
        """
        chat = db.get(Chat, chat_id)
        if chat:
            chat.title = title
            db.commit()
            db.refresh(chat)
        return chat

    def mark_as_completed(self, db: Session, chat_id: int) -> Chat | None:
        """
        Mark a chat as completed (finalized interview).
        
        Args:
            db (Session): Database session.
            chat_id (int): ID of the chat.
            
        Returns:
            Chat | None: The updated chat object if found, else None.
        """
        from sqlalchemy import func
        chat = db.get(Chat, chat_id)
        if chat:
            chat.status = "completed"
            chat.completed_at = func.now()
            db.commit()
            db.refresh(chat)
        return chat

chat_repo = ChatRepo()
