# app/services/message_service.py
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.message_repo import message_repo
from app.services.chat_service import chat_service
from app.models.message import Message


class MessageService:
    def list_messages(self, db: Session, chat_id: int, user_id: int, limit: int = 50) -> list[Message]:
        """Retrieve messages for a chat (validates ownership)."""
        chat_service.get_chat_for_user_or_404(db, chat_id, user_id)
        return message_repo.list_for_chat(db, chat_id, limit=limit)

    def create_user_message(self, db: Session, chat_id: int, user_id: int, contenido: str) -> Message:
        """Create a user message (validates chat ownership and content)."""
        if not contenido or not contenido.strip():
            raise HTTPException(status_code=422, detail="Message content cannot be empty")

        chat_service.get_chat_for_user_or_404(db, chat_id, user_id)
        return message_repo.create(db, chat_id, "USER", contenido.strip())

    def create_ai_message(self, db: Session, chat_id: int, user_id: int, contenido: str) -> Message:
        """Create an AI message (validates chat ownership and content)."""
        if not contenido or not contenido.strip():
            raise HTTPException(status_code=500, detail="AI response was empty")

        chat_service.get_chat_for_user_or_404(db, chat_id, user_id)
        return message_repo.create(db, chat_id, "IA", contenido.strip())

    def build_bedrock_history(self, db: Session, chat_id: int, user_id: int, limit: int = 50) -> list[dict]:
        """Build Bedrock API message history in [{"role": "user"|"assistant", "content": "..."}] format (chronological order)."""
        chat_service.get_chat_for_user_or_404(db, chat_id, user_id)
        msgs = message_repo.list_for_chat(db, chat_id, limit=limit)
        msgs = list(reversed(msgs))

        history: list[dict] = []
        for m in msgs:
            role = "user" if m.emisor == "USER" else "assistant"
            history.append({"role": role, "content": m.contenido})
        return history


message_service = MessageService()
