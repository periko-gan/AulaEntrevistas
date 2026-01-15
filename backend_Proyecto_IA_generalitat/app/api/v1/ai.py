from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import logging

from app.core.database import get_db
from app.api.deps import get_current_user
from app.repositories.chat_repo import chat_repo
from app.repositories.message_repo import message_repo
from app.schemas.ai import AiReplyRequest, InitializeChatRequest
from app.schemas.message import MessageResponse
from app.services.ai.bedrock_service import bedrock_chat, generate_initial_greeting
from app.services.message_service import message_service

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/initialize", response_model=MessageResponse)
def initialize_chat(payload: InitializeChatRequest, db: Session = Depends(get_db), user=Depends(get_current_user)):
    """Initialize a chat with Evalio's greeting message.
    
    This endpoint creates the first AI message in a chat with the presentation.
    """
    chat = chat_repo.get_for_user(db, payload.chat_id, user.id_usuario)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")

    try:
        # Generate initial greeting from Evalio
        greeting = generate_initial_greeting()
        
        # Save AI greeting message
        ia_msg = message_repo.create(db, payload.chat_id, "IA", greeting)
        logger.info(f"Initial greeting created: {ia_msg.id_mensaje}")
        
        db.commit()
        
        return ia_msg
        
    except Exception as e:
        db.rollback()
        logger.error(f"Error initializing chat: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Error initializing chat")


@router.post("/reply", response_model=MessageResponse)
def ai_reply(payload: AiReplyRequest, db: Session = Depends(get_db), user=Depends(get_current_user)):
    """Generate an AI reply to a user message in a chat.
    
    This endpoint is atomic: if any step fails (Bedrock error, DB error),
    both user and AI messages are rolled back to maintain data integrity.
    """
    chat = chat_repo.get_for_user(db, payload.chat_id, user.id_usuario)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")

    try:
        # Step 1: Save user message
        user_msg = message_repo.create(db, payload.chat_id, "USER", payload.contenido)
        logger.info(f"User message created: {user_msg.id_mensaje}")
        
        # Step 2: Generate AI response
        history = message_service.build_bedrock_history(db, payload.chat_id, user.id_usuario, limit=50)
        ai_text = bedrock_chat(history)
        
        # Step 3: Save AI message
        ia_msg = message_repo.create(db, payload.chat_id, "IA", ai_text)
        logger.info(f"AI message created: {ia_msg.id_mensaje}")
        
        # Step 4: Commit atomic transaction
        db.commit()
        
        return ia_msg
        
    except Exception as e:
        db.rollback()
        logger.error(f"Error in AI reply: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Error generating reply")
