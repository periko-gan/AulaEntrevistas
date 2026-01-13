from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.deps import get_current_user
from app.schemas.chat import ChatResponse, CreateChatResponse
from app.services.chat_service import chat_service
from app.repositories.chat_repo import chat_repo

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


@router.get("/{chat_id}", response_model=ChatResponse)
def get_chat(
    chat_id: int = Path(..., ge=1),
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    """Retrieve a specific chat (validates ownership)."""
    chat = chat_repo.get_for_user(db, chat_id, user.id_usuario)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    return chat


@router.delete("/{chat_id}")
def delete_chat(
    chat_id: int = Path(..., ge=1),
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    """Delete a chat (validates ownership)."""
    chat = chat_repo.get_for_user(db, chat_id, user.id_usuario)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    
    chat_repo.delete(db, chat_id)
    return {"message": "Chat deleted successfully"}
