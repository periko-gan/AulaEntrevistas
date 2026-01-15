# app/services/chat_service.py
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.chat_repo import chat_repo
from app.models.chat import Chat


class ChatService:
    def create_chat(self, db: Session, user_id: int) -> Chat:
        """Create a new chat for the user."""
        return chat_repo.create(db, user_id)

    def list_chats(self, db: Session, user_id: int) -> list[Chat]:
        """Retrieve all chats for the user."""
        return chat_repo.list_for_user(db, user_id)

    def get_chat_for_user_or_404(self, db: Session, chat_id: int, user_id: int) -> Chat:
        """Validate that the chat exists and belongs to the user."""
        chat = chat_repo.get_for_user(db, chat_id, user_id)
        if not chat:
            raise HTTPException(status_code=404, detail="Chat not found")
        return chat

    def update_chat_title(self, db: Session, chat_id: int, user_id: int, title: str) -> Chat:
        """Update the title of a chat (validates ownership)."""
        chat = self.get_chat_for_user_or_404(db, chat_id, user_id)
        return chat_repo.update_title(db, chat_id, title)


chat_service = ChatService()
