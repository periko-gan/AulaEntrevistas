from sqlalchemy import Text, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from datetime import datetime

class Message(Base):
    __tablename__ = "mensajes"

    id_mensaje: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    id_chat: Mapped[int] = mapped_column(ForeignKey("chats.id_chat"), nullable=False, index=True)
    emisor: Mapped[str] = mapped_column(Text(10), nullable=False)  # "USER" | "IA"
    contenido: Mapped[str] = mapped_column(Text, nullable=False)
    sent_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    chat = relationship("Chat", back_populates="mensajes")
