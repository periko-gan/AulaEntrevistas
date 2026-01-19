from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from slowapi import Limiter
from slowapi.util import get_remote_address
import logging
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

    try:
        # Build conversation history
        history = message_service.build_bedrock_history(db, payload.chat_id, user.id_usuario, limit=100)
        
        # Generate final report with AI (with higher max_tokens for comprehensive report)
        report_prompt = {
            "role": "user",
            "content": (
                "La entrevista ha finalizado. Por favor, genera el informe completo de evaluación "
                "siguiendo ESTRICTAMENTE el formato establecido en las directrices del sistema. "
                "IMPORTANTE: "
                "1. Incluye OBLIGATORIAMENTE al inicio la sección 'DATOS DE LA ENTREVISTA' con los valores REALES "
                "   que el candidato proporcionó (NO uses placeholders como [fecha actual] o [rol proporcionado]). "
                "   Usa los valores específicos: Fecha, Rol laboral simulado, Nivel académico, Ciclo formativo, Duración. "
                "2. Sé REALISTA y CRÍTICO en tu evaluación. NO suavices errores graves. "
                "3. Si el candidato cometió errores conceptuales graves, indícalo claramente en 'Errores críticos' "
                "   con ejemplos ESPECÍFICOS de lo que dijo mal. "
                "4. En ortografía, indica el NÚMERO EXACTO de faltas detectadas y lista EJEMPLOS ESPECÍFICOS "
                "   de palabras mal escritas (NO uses placeholders como [número de errores] o [listar errores]). "
                "5. El nivel de empleabilidad debe reflejar el desempeño REAL basado en lo observado: "
                "   - Muy bajo: múltiples errores graves "
                "   - Bajo: errores importantes en conceptos básicos "
                "   - Medio: conocimientos aceptables con lagunas "
                "   - Bueno: buen dominio con pocas lagunas "
                "   - Muy bueno: dominio excelente (usar solo si realmente aplica) "
                "6. NO uses placeholders ni texto genérico. Todo debe ser específico y basado en la entrevista real. "
                "7. Incluye TODAS las secciones: valoración general, puntos fuertes (solo si existen), "
                "   errores críticos, aspectos a mejorar, ortografía, recomendaciones, impacto en entrevista real, "
                "   acciones prioritarias (7 días) y nivel de empleabilidad."
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
        
        for msg in messages[:20]:  # Check first 20 messages for config data
            content_lower = msg.contenido.lower()
            
            # Detect rol laboral
            if any(word in content_lower for word in ['junior', 'middle', 'senior']):
                if 'junior' in content_lower:
                    rol_laboral = "Junior"
                elif 'middle' in content_lower:
                    rol_laboral = "Middle"
                elif 'senior' in content_lower:
                    rol_laboral = "Senior"
            
            # Detect nivel académico
            if 'fp básica' in content_lower or 'fp basica' in content_lower:
                nivel_academico = "FP Básica"
            elif 'fp media' in content_lower:
                nivel_academico = "FP Media"
            elif 'fp superior' in content_lower:
                nivel_academico = "FP Superior"
            elif 'máster' in content_lower or 'master' in content_lower:
                nivel_academico = "Máster/Especialización"
            
            # Detect duración
            if 'corta' in content_lower:
                duracion = "Corta"
            elif 'media' in content_lower and 'duraci' in content_lower:
                duracion = "Media"
            elif 'larga' in content_lower:
                duracion = "Larga"
            
            # Detect ciclo formativo específico (buscar siglas y nombres comunes)
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
            
            for sigla, nombre_completo in ciclos_conocidos.items():
                if sigla in content_lower:
                    ciclo_formativo = nombre_completo
                    break
            
            # Si no se detectó un ciclo conocido, intentar extraer lo que dijo el usuario
            if ciclo_formativo == "No especificado" and msg.emisor == "USER":
                # Buscar líneas que parezcan respuestas a "qué ciclo formativo"
                if len(msg.contenido) > 3 and len(msg.contenido) < 100:
                    # Probablemente es una respuesta corta de configuración
                    if any(palabra in content_lower for palabra in ['ciclo', 'estudio', 'estudiando', 'formativo']):
                        ciclo_formativo = msg.contenido
        
        # Generate PDF
        pdf_buffer = generate_pdf_report(
            report_content=report_content,
            candidate_name=user.nombre,
            rol_laboral=rol_laboral,
            nivel_academico=nivel_academico,
            ciclo_formativo=ciclo_formativo,
            duracion=duracion,
            interview_date=chat.created_at
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
