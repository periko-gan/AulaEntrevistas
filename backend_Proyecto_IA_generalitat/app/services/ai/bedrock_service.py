# app/services/ai/bedrock_service.py
import os
import logging
import boto3
import re
from botocore.exceptions import BotoCoreError, ClientError
from pathlib import Path
from sqlalchemy.orm import Session

from app.core.config import settings

# Configure logging
logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent
SYSTEM_PROMPT = (BASE_DIR / "system_prompt.txt").read_text(encoding="utf-8").strip()

AWS_REGION = os.getenv("AWS_REGION") or getattr(settings, "aws_region", None) or "us-east-1"
BEDROCK_MODEL_ID = os.getenv("BEDROCK_MODEL_ID") or getattr(settings, "bedrock_model_id", None) or "amazon.nova-micro-v1:0"

AGENT_ID = os.getenv("BEDROCK_AGENT_ID") or "YWPZKUZ1W2"
AGENT_ALIAS_ID = os.getenv("BEDROCK_AGENT_ALIAS_ID") or "AG2TCM3LTP"

_client = boto3.client("bedrock-agent-runtime", region_name=AWS_REGION)

# Robust separator to prevent prompt injection
SYSTEM_SEPARATOR = "\n" + "=" * 60 + "\n[SYSTEM CONTEXT]\n" + "=" * 60 + "\n"
CONTEXT_END_SEPARATOR = "\n" + "=" * 60 + "\n[END SYSTEM CONTEXT]\n" + "=" * 60 + "\n"



def _sanitize_user_input(text: str) -> str:
    """
    Sanitize user input to prevent common prompt injection attacks.
    Uses word boundary detection to avoid false positives.
    
    Args:
        text: User input text to sanitize
        
    Returns:
        Sanitized text
        
    Raises:
        ValueError: If input contains potential injection patterns
    """
    import re
    
    text_lower = text.lower()
    
    # Multi-word phrases (more specific, less false positives)
    # These must appear as complete phrases
    phrase_patterns = [
        r'\bignore\s+(?:the\s+)?instructions?\b',
        r'\bforgot?\s+(?:the\s+)?(?:system|instructions?|prompt)\b',
        r'\bshow\s+(?:me\s+)?(?:the\s+)?(?:system|prompt|instructions?)\b',
        r'\breveal\s+(?:the\s+)?(?:system|prompt|instructions?)\b',
        r'\bsystem\s+prompt\b',
        r'\bsystem\s+instructions?\b',
        r'\boverride\s+(?:the\s+)?(?:system|instructions?)\b',
        r'\bbypass\s+(?:the\s+)?(?:system|instructions?|security)\b',
        r'\bjailbreak\b',
        # Spanish phrases
        r'\bignora\s+(?:las?\s+)?(?:instrucciones?|indicaciones?)\b',
        r'\bolvid[aáe].*?(?:instrucciones?|sistema|prompt)\b',
        r'\bolvídate\s+(?:del?\s+)?(?:sistema|prompt)\b',
        r'\bolvída\s+(?:lo\s+)?(?:anterior|del\s+sistema)\b',
        r'\brevela\s+(?:el?\s+)?(?:sistema|prompt|las?\s+instrucciones?)\b',
        r'\bcuéntame\s+(?:el?\s+)?(?:sistema|prompt)\b',
        r'\bdime\s+(?:el?\s+)?(?:sistema|prompt|las?\s+instrucciones?)\b',
        r'\bmuéstrame\s+(?:el?\s+)?(?:sistema|prompt|las?\s+instrucciones?)\b',
        r'\bdesactive\s+(?:la?\s+)?(?:protección|seguridad)\b',
        r'\banula\s+(?:las?\s+)?(?:instrucciones?|indicaciones?)\b',
    ]
    
    found_patterns = []
    for pattern in phrase_patterns:
        if re.search(pattern, text_lower):
            found_patterns.append(pattern.replace(r'\b', '').split('\\s')[0])
    
    if found_patterns:
        logger.warning(
            f"Potential prompt injection detected in user input. Patterns found: {found_patterns}"
        )
        raise ValueError(
            f"Input contains restricted patterns. Please rephrase your question."
        )
    
    return text.strip()


def generate_reply(
    history: list[dict],
    chat_id: int,
    max_tokens: int = 200,
    temperature: float = 0.7,
    top_p: float = 0.9,
) -> str:
    """Generate an AI reply using AWS Bedrock Agent with prompt injection protection.
    
    Args:
        history: List of message dictionaries with 'role' and 'content' keys
        chat_id: Chat ID to use as session ID for the agent
        max_tokens: Maximum tokens in response (default: 200)
        temperature: Sampling temperature 0.0-1.0 (default: 0.7)
        top_p: Nucleus sampling parameter (default: 0.9)
        
    Returns:
        Generated AI response text
        
    Raises:
        ValueError: If prompt injection is detected
        RuntimeError: If Bedrock Agent API call fails
    """
    # Get the last user message from history
    user_message = ""
    for m in reversed(history):
        if m.get("role") == "user":
            content = m.get("content", "").strip()
            # Sanitize user input to prevent prompt injection
            try:
                user_message = _sanitize_user_input(content)
            except ValueError as e:
                logger.error(f"Input validation failed: {str(e)}")
                raise
            break
    
    if not user_message:
        raise ValueError("No user message found in history")

    try:
        # Invoke the Bedrock Agent
        session_id = f"chat_{chat_id}"  # Format: "chat_1", "chat_2", etc. (min 2 chars)
        
        logger.info(f"🤖 USING BEDROCK AGENT - AgentID: {AGENT_ID}, AliasID: {AGENT_ALIAS_ID}, SessionID: {session_id}")
        logger.info(f"📝 User message: {user_message}")
        
        resp = _client.invoke_agent(
            agentId=AGENT_ID,
            agentAliasId=AGENT_ALIAS_ID,
            sessionId=session_id,
            inputText=user_message,
        )
        
        logger.info(f"✅ Bedrock Agent API call successful")
        
    except (ClientError, BotoCoreError) as e:
        logger.error(
            f"❌ Bedrock Agent API error: {str(e)}",
            extra={
                "agent_id": AGENT_ID,
                "region": AWS_REGION,
                "error_type": type(e).__name__
            },
            exc_info=True
        )
        raise RuntimeError(f"Failed to generate AI response: {str(e)}")

    # Parse the response stream and accumulate text chunks
    text = ""
    chunk_count = 0
    try:
        for event in resp.get("completion", []):
            if "chunk" in event:
                chunk_data = event["chunk"]
                if "bytes" in chunk_data:
                    # Decode bytes to string and accumulate
                    chunk_text = chunk_data["bytes"].decode("utf-8")
                    text += chunk_text
                    chunk_count += 1
                    logger.debug(f"📦 Chunk {chunk_count}: {len(chunk_text)} chars")
        
        logger.info(f"✨ Agent response complete - Total chunks: {chunk_count}, Total response length: {len(text)}")
        
    except Exception as e:
        logger.error(f"Error parsing agent response stream: {str(e)}", exc_info=True)
        raise RuntimeError(f"Failed to parse agent response: {str(e)}")

    return text.strip() or "Unable to generate a response at this moment."


def bedrock_chat(history: list[dict], chat_id: int) -> str:
    """Wrapper function to generate a reply with default parameters."""
    return generate_reply(history, chat_id)


def is_interview_completed(response_text: str) -> bool:
    """Detecta si el agente ha indicado que la entrevista finalizó.
    
    Args:
        response_text: Texto de respuesta del agente
        
    Returns:
        True si se detecta el marcador de finalización, False en caso contrario
    """
    pattern = r'\*\*ENTREVISTA_FINALIZADA\*\*'
    found = bool(re.search(pattern, response_text))
    if found:
        logger.info("🎯 Marcador de finalización de entrevista detectado")
    return found


def mark_chat_completed(db: Session, chat_id: int) -> None:
    """Marca un chat como completado en la base de datos.
    
    Args:
        db: Sesión de base de datos
        chat_id: ID del chat a marcar como completado
    """
    from app.repositories.chat_repo import chat_repo
    from datetime import datetime
    
    try:
        chat = db.get(chat_repo.__class__.__annotations__['create'].__args__[0].__args__[1], chat_id)
        if not chat:
            # Usar el método del repositorio si existe
            from app.models.chat import Chat
            chat = db.get(Chat, chat_id)
        
        if chat and chat.status != "completed":
            chat.status = "completed"
            chat.completed_at = datetime.now()
            db.commit()
            logger.info(f"✅ Chat {chat_id} marcado como completado automáticamente")
    except Exception as e:
        db.rollback()
        logger.error(f"❌ Error al marcar chat {chat_id} como completado: {str(e)}")
        raise


def generate_initial_greeting() -> str:
    """Generate the initial greeting message from Evalio.
    
    Returns:
        Initial greeting text introducing Evalio and the interview process
    """
    greeting = """¡Hola! Soy **Evalio**, tu simulador de entrevistas técnicas para Formación Profesional. 

Mi objetivo es ayudarte a prepararte para entrevistas laborales reales mediante una simulación conversacional adaptada a tu nivel y especialidad.

Antes de comenzar, necesito hacerte 4 preguntas para personalizar la entrevista según tu perfil. Una vez configurada, te haré preguntas técnicas y evaluaré tus competencias de forma realista y constructiva.

Al finalizar, recibirás un informe detallado con recomendaciones concretas para mejorar tu empleabilidad.

Escribe "empezar" cuando estés listo/a para comenzar."""
    
    return greeting
