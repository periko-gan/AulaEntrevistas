from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.chat import Chat

class ChatRepo:
    def create(self, db: Session, user_id: int) -> Chat:
        """Create a new chat for a user."""
        chat = Chat(id_usuario=user_id)
        db.add(chat)
        db.commit()
        db.refresh(chat)
        return chat

    def list_for_user(self, db: Session, user_id: int) -> list[Chat]:
        """Retrieve all chats for a user, ordered by most recent first."""
        return list(db.scalars(select(Chat).where(Chat.id_usuario == user_id).order_by(Chat.created_at.desc())))

    def get_for_user(self, db: Session, chat_id: int, user_id: int) -> Chat | None:
        """Retrieve a specific chat if it belongs to the user."""
        return db.scalar(select(Chat).where(Chat.id_chat == chat_id, Chat.id_usuario == user_id))

    def delete(self, db: Session, chat_id: int) -> None:
        """Delete a chat and all its messages (cascade)."""
        chat = db.get(Chat, chat_id)
        if chat:
            db.delete(chat)
            db.commit()

chat_repo = ChatRepo()
