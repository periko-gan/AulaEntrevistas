from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.deps import get_current_user
from app.schemas.chat import ChatResponse, CreateChatResponse
from app.services.chat_service import chat_service

router = APIRouter()

@router.post("", response_model=CreateChatResponse)
def create_chat(db: Session = Depends(get_db), user=Depends(get_current_user)):
    """Create a new chat for the authenticated user."""
    chat = chat_service.create_chat(db, user.id_usuario)
    return CreateChatResponse(id_chat=chat.id_chat)

@router.get("", response_model=list[ChatResponse])
def list_chats(db: Session = Depends(get_db), user=Depends(get_current_user)):
    """Retrieve all chats for the authenticated user."""
    return chat_service.list_chats(db, user.id_usuario)
