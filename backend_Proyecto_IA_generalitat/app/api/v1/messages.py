from fastapi import APIRouter, Depends, HTTPException, Query, Body
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.deps import get_current_user
from app.repositories.chat_repo import chat_repo
from app.repositories.message_repo import message_repo
from app.schemas.message import MessageResponse, CreateMessageRequest

router = APIRouter()

@router.get("", response_model=list[MessageResponse])
def list_messages(
    chat_id: int = Query(...),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    """Retrieve messages from a chat (validates chat ownership)."""
    chat = chat_repo.get_for_user(db, chat_id, user.id_usuario)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    return message_repo.list_for_chat(db, chat_id, limit=limit)

@router.post("", response_model=MessageResponse)
def create_message(
    chat_id: int = Query(...),
    payload: CreateMessageRequest = Body(...),
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    """Create a new user message in a chat (validates chat ownership)."""
    chat = chat_repo.get_for_user(db, chat_id, user.id_usuario)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    return message_repo.create(db, chat_id, "USER", payload.contenido)
