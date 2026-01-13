from pydantic import BaseModel, Field
from datetime import datetime
from typing import Literal

class MessageResponse(BaseModel):
    id_mensaje: int
    id_chat: int
    emisor: Literal["USER", "IA"]
    contenido: str
    sent_at: datetime

    class Config:
        from_attributes = True

class CreateMessageRequest(BaseModel):
    contenido: str = Field(min_length=1, max_length=8000)
