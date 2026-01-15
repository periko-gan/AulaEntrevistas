from sqlalchemy import DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from datetime import datetime

class Chat(Base):
    __tablename__ = "chats"

    id_chat: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    id_usuario: Mapped[int] = mapped_column(ForeignKey("users.id_usuario"), nullable=False, index=True)
    title: Mapped[str | None] = mapped_column(nullable=False, default="Nuevo Chat")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    last_message_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    user = relationship("User", back_populates="chats")
    mensajes = relationship("Message", back_populates="chat", cascade="all, delete-orphan")
