from sqlalchemy.orm import Session
from sqlalchemy import select, func
from app.models.message import Message
from app.models.chat import Chat

class MessageRepo:
    def list_for_chat(self, db: Session, chat_id: int, limit: int = 50) -> list[Message]:
        """Retrieve messages for a chat in descending order by timestamp."""
        stmt = select(Message).where(Message.id_chat == chat_id).order_by(Message.sent_at.desc()).limit(limit)
        return list(db.scalars(stmt))

    def create(self, db: Session, chat_id: int, emisor: str, contenido: str) -> Message:
        """Create a new message and update the chat's last_message_at timestamp."""
        msg = Message(id_chat=chat_id, emisor=emisor, contenido=contenido)
        db.add(msg)

        chat = db.get(Chat, chat_id)
        if chat:
            chat.last_message_at = func.now()

        db.commit()
        db.refresh(msg)
        return msg

message_repo = MessageRepo()
