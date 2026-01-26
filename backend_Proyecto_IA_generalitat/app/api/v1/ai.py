from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from slowapi import Limiter
from slowapi.util import get_remote_address
import logging
import re
from datetime import datetime

from app.core.database import get_db
from app.api.deps import get_current_user
from app.repositories.chat_repo import chat_repo
from app.repositories.message_repo import message_repo
from app.schemas.ai import AiReplyRequest, InitializeChatRequest, GenerateReportRequest
from app.schemas.message import MessageResponse
from app.services.ai.bedrock_service import bedrock_chat, generate_initial_greeting, generate_reply
from app.services.ai.pdf_service import generate_pdf_report
from app.services.message_service import message_service

logger = logging.getLogger(__name__)
limiter = Limiter(key_func=get_remote_address)

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
@limiter.limit("15/minute")  # Max 15 mensajes por minuto por IP
def ai_reply(request: Request, payload: AiReplyRequest, db: Session = Depends(get_db), user=Depends(get_current_user)):
    """Generate an AI reply to a user message in a chat.
    
    This endpoint is atomic: if any step fails (Bedrock error, DB error),
    both user and AI messages are rolled back to maintain data integrity.
    """
    chat = chat_repo.get_for_user(db, payload.chat_id, user.id_usuario)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    
    # Check if chat is completed
    if chat.status == "completed":
        raise HTTPException(
            status_code=400, 
            detail="Esta entrevista ha finalizado. No se pueden enviar más mensajes. Crea una nueva entrevista para continuar."
        )

    try:
        # Step 1: Save user message
        user_msg = message_repo.create(db, payload.chat_id, "USER", payload.contenido)
        logger.info(f"User message created: {user_msg.id_mensaje}")
        
        # Step 2: Generate AI response
        history = message_service.build_bedrock_history(db, payload.chat_id, user.id_usuario, limit=50)
        ai_text = bedrock_chat(history, payload.chat_id)
        
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


@router.post("/generate-report")
@limiter.limit("3/hour")  # Max 3 PDFs por hora por IP
def generate_interview_report(
    request: Request,
    payload: GenerateReportRequest,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    """Generate a PDF report of the interview evaluation.
    
    This endpoint:
    1. Retrieves all messages from the chat
    2. Asks the AI to generate a final comprehensive report
    3. Converts the report to a professional PDF
    4. Returns the PDF as a downloadable file
    """
    chat = chat_repo.get_for_user(db, payload.chat_id, user.id_usuario)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")

    # Validate that there are enough messages for a report
    messages = message_repo.list_for_chat(db, payload.chat_id, limit=100)
    if len(messages) < 5:
        raise HTTPException(
            status_code=400, 
            detail="No se puede generar un informe sin haber realizado la entrevista. Necesitas al menos completar la configuración inicial y responder algunas preguntas."
        )

    try:
        # Build conversation history
        history = message_service.build_bedrock_history(db, payload.chat_id, user.id_usuario, limit=100)
        
        # Generate final report with AI (with higher max_tokens for comprehensive report)
        report_prompt = {
            "role": "user",
            "content": (
                "La entrevista ha finalizado. Por favor, genera el informe completo de evaluación "
                "siguiendo ESTRICTAMENTE estas reglas: "
                "\n"
                "🚫 PROHIBICIONES ABSOLUTAS: "
                "1. ❌ NO incluyas NUNCA la sección 'DATOS DE LA ENTREVISTA' ni sus datos (candidato, fecha, rol, nivel, ciclo, duración). "
                "   Estos datos se renderizan automáticamente en el header del PDF. "
                "2. ❌ NO incluyas bullets (-, •, *) con metadatos del candidato. "
                "3. ❌ NO uses placeholders como [fecha], [rol], [ciclo], etc. "
                "4. ❌ NO incluyas JSON, código, bloques técnicos ni formatos especiales. "
                "\n"
                "✅ CONTENIDO REQUERIDO (comienza DIRECTAMENTE con esto): "
                "5. El informe comienza CON 'Valoración general del perfil'. NO hay introducción previa. "
                "6. Sé REALISTA y CRÍTICO. NO suavices errores graves. Trata como incorrectas las respuestas incorrectas. "
                "\n"
                "📝 DETALLES POR SECCIÓN: "
                "7. Ortografía: Registra SOLO faltas alfabéticas (no emojis, URLs, código). "
                "   Formato: 'palabra escrita mal' en lugar de 'palabra correcta'. "
                "8. Errores conceptuales: indícalos en 'Errores críticos' con ejemplos EXACTOS de qué dijo mal. "
                "9. Empleabilidad: usa UNA SOLA de: Muy bajo | Bajo | Medio | Bueno | Muy bueno. "
                "   Refleja el desempeño REAL. 'Muy bueno' solo si realmente merece 95+/100. "
                "\n"
                "📋 SECCIONES A INCLUIR (usa estos títulos con ##): "
                "   ## Valoración general "
                "   ## Puntos fuertes (omitir si no existen) "
                "   ## Errores críticos (omitir si no los hay) "
                "   ## Aspectos a mejorar "
                "   ## Ortografía y expresión escrita "
                "   ## Recomendaciones prácticas "
                "   ## Impacto en una entrevista real "
                "   ## Acciones prioritarias (próximos 7 días) "
                "   ## Nivel estimado de empleabilidad "
            )
        }
        history.append(report_prompt)
        
        report_content = generate_reply(history, max_tokens=2500, temperature=0.7)
        logger.info(f"AI report generated for chat {payload.chat_id}")
        
        # Extract metadata from chat history for PDF
        # Messages already loaded for validation above
        rol_laboral = "No especificado"
        nivel_academico = "No especificado"
        ciclo_formativo = "No especificado"
        duracion = "No especificada"
        
        logger.info(f"Extracting metadata from {len(messages)} messages")
        
        for idx, msg in enumerate(messages[:30]):  # Check first 30 messages for config data
            if not msg.contenido:
                continue
                
            content_lower = msg.contenido.lower()
            content_clean = msg.contenido.strip()
            
            # DETECT ROL LABORAL (more flexible matching)
            if rol_laboral == "No especificado":
                # Look for role keywords (case-insensitive, whole words)
                if re.search(r'\bjunior\b', content_lower):
                    rol_laboral = "Junior"
                    logger.info(f"Detected rol_laboral='Junior' from message {idx}")
                elif re.search(r'\bmiddle\b', content_lower):
                    rol_laboral = "Middle"
                    logger.info(f"Detected rol_laboral='Middle' from message {idx}")
                elif re.search(r'\bsenior\b', content_lower):
                    rol_laboral = "Senior"
                    logger.info(f"Detected rol_laboral='Senior' from message {idx}")
            
            # DETECT NIVEL ACADÉMICO (more flexible matching)
            if nivel_academico == "No especificado":
                if 'fp básica' in content_lower or 'fp basica' in content_lower or 'fp básico' in content_lower:
                    nivel_academico = "FP Básica"
                    logger.info(f"Detected nivel_academico='FP Básica' from message {idx}")
                elif 'fp media' in content_lower or 'fp medio' in content_lower:
                    nivel_academico = "FP Media"
                    logger.info(f"Detected nivel_academico='FP Media' from message {idx}")
                elif 'fp superior' in content_lower:
                    nivel_academico = "FP Superior"
                    logger.info(f"Detected nivel_academico='FP Superior' from message {idx}")
                elif 'máster' in content_lower or 'master' in content_lower or 'especialización' in content_lower or 'especializacion' in content_lower:
                    nivel_academico = "Máster/Especialización"
                    logger.info(f"Detected nivel_academico='Máster/Especialización' from message {idx}")
                # Capture generic "FP" if nothing else matched and this looks like a config response
                elif re.search(r'\bfp\b', content_lower) and len(content_clean) < 50:
                    nivel_academico = "FP"
                    logger.info(f"Detected nivel_academico='FP' (generic) from message {idx}")
            
            # DETECT DURACIÓN (more flexible matching - look for the word alone, not combined with others)
            if duracion == "No especificada":
                if re.search(r'\bcorta\b', content_lower):
                    duracion = "Corta"
                    logger.info(f"Detected duracion='Corta' from message {idx}")
                elif re.search(r'\bmedia\b', content_lower):
                    duracion = "Media"
                    logger.info(f"Detected duracion='Media' from message {idx}")
                elif re.search(r'\blarga\b', content_lower):
                    duracion = "Larga"
                    logger.info(f"Detected duracion='Larga' from message {idx}")
            
            # DETECT CICLO FORMATIVO (buscar siglas y nombres comunes)
            if ciclo_formativo == "No especificado":
                ciclos_conocidos = {
                    'daw': 'DAW - Desarrollo de Aplicaciones Web',
                    'dam': 'DAM - Desarrollo de Aplicaciones Multiplataforma',
                    'asir': 'ASIR - Administración de Sistemas Informáticos en Red',
                    'smr': 'SMR - Sistemas Microinformáticos y Redes',
                    'enfermería': 'Enfermería',
                    'enfermeria': 'Enfermería',
                    'integración social': 'Integración Social',
                    'integracion social': 'Integración Social',
                    'electrónica': 'Electrónica Industrial',
                    'electronica': 'Electrónica Industrial',
                    'administración y finanzas': 'Administración y Finanzas',
                    'administracion y finanzas': 'Administración y Finanzas',
                    'comercio internacional': 'Comercio Internacional',
                    'marketing': 'Marketing y Publicidad',
                    'auxiliar de enfermería': 'Auxiliar de Enfermería',
                    'auxiliar de enfermeria': 'Auxiliar de Enfermería'
                }
                
                # Try to find known ciclos first
                for sigla, nombre_completo in ciclos_conocidos.items():
                    if sigla in content_lower:
                        ciclo_formativo = nombre_completo
                        logger.info(f"Detected ciclo_formativo='{nombre_completo}' from message {idx}")
                        break
                
                # If no known ciclo detected but this looks like a config response, capture it
                if ciclo_formativo == "No especificado" and msg.emisor == "USER":
                    # Check if this is likely a ciclo response (short message, likely between messages 4-12)
                    if 3 < len(content_clean) < 150 and idx >= 3:
                        # Only capture if it doesn't contain question marks or common non-response words
                        if '?' not in msg.contenido and len(content_clean) > 0:
                            # Check if it contains ciclo-related keywords
                            if any(palabra in content_lower for palabra in ['ciclo', 'estudio', 'estudiando', 'formativo', 'carrera', 'especialidad', 'técnico']):
                                ciclo_formativo = content_clean
                                logger.info(f"Detected ciclo_formativo='{content_clean}' (custom) from message {idx}")
        
        # Generate PDF
        pdf_buffer = generate_pdf_report(
            report_content=report_content,
            candidate_name=user.nombre,
            rol_laboral=rol_laboral,
            nivel_academico=nivel_academico,
            ciclo_formativo=ciclo_formativo,
            duracion=duracion,
            interview_date=chat.created_at,
            messages=messages
        )
        
        # Mark chat as completed
        chat_repo.mark_as_completed(db, payload.chat_id)
        logger.info(f"Chat {payload.chat_id} marked as completed")
        
        # Return PDF as downloadable file
        filename = f"informe_entrevista_{payload.chat_id}_{datetime.now().strftime('%Y%m%d')}.pdf"
        
        return StreamingResponse(
            pdf_buffer,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename={filename}"
            }
        )
        
    except ValueError as e:
        logger.error(f"Validation error generating report: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error generating report: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Error generating report")
