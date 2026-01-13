from pydantic import BaseModel
from datetime import datetime

class ChatResponse(BaseModel):
    id_chat: int
    id_usuario: int
    title: str
    created_at: datetime
    last_message_at: datetime | None

    class Config:
        from_attributes = True

class CreateChatResponse(BaseModel):
    id_chat: int
