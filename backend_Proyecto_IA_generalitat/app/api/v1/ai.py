from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.deps import get_current_user
from app.repositories.chat_repo import chat_repo
from app.repositories.message_repo import message_repo
from app.schemas.ai import AiReplyRequest
from app.schemas.message import MessageResponse
from app.services.ai.bedrock_service import bedrock_chat

router = APIRouter()

def _build_history_for_bedrock(db: Session, chat_id: int, limit: int = 50) -> list[dict]:
    """Build Bedrock message history in chronological order."""
    msgs = message_repo.list_for_chat(db, chat_id, limit=limit)
    msgs = list(reversed(msgs))

    history: list[dict] = []
    for m in msgs:
        role = "user" if m.emisor == "USER" else "assistant"
        history.append({"role": role, "content": m.contenido})
    return history


@router.post("/reply", response_model=MessageResponse)
def ai_reply(payload: AiReplyRequest, db: Session = Depends(get_db), user=Depends(get_current_user)):
    """Generate an AI reply to a user message in a chat."""
    chat = chat_repo.get_for_user(db, payload.chat_id, user.id_usuario)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")

    message_repo.create(db, payload.chat_id, "USER", payload.contenido)

    history = _build_history_for_bedrock(db, payload.chat_id, limit=50)
    ai_text = bedrock_chat(history)

    ia_msg = message_repo.create(db, payload.chat_id, "IA", ai_text)
    return ia_msg
