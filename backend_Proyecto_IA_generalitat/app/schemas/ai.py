from pydantic import BaseModel, Field

class AiReplyRequest(BaseModel):
    chat_id: int = Field(..., ge=1)
    contenido: str = Field(..., min_length=1, max_length=8000)

class InitializeChatRequest(BaseModel):
    chat_id: int = Field(..., ge=1)
