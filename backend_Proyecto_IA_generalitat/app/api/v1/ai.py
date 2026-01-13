from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.deps import get_current_user
from app.repositories.chat_repo import chat_repo
from app.repositories.message_repo import message_repo
from app.schemas.ai import AiReplyRequest
from app.schemas.message import MessageResponse
from app.services.ai.bedrock_service import bedrock_chat
from app.services.message_service import message_service

router = APIRouter()


@router.post("/reply", response_model=MessageResponse)
def ai_reply(payload: AiReplyRequest, db: Session = Depends(get_db), user=Depends(get_current_user)):
    """Generate an AI reply to a user message in a chat."""
    chat = chat_repo.get_for_user(db, payload.chat_id, user.id_usuario)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")

    message_repo.create(db, payload.chat_id, "USER", payload.contenido)

    history = message_service.build_bedrock_history(db, payload.chat_id, user.id_usuario, limit=50)
    ai_text = bedrock_chat(history)

    ia_msg = message_repo.create(db, payload.chat_id, "IA", ai_text)
    return ia_msg
