from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.deps import get_current_user
from app.repositories.chat_repo import chat_repo
from app.repositories.message_repo import message_repo
from app.schemas.message import MessageResponse

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
