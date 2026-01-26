from weasyprint import HTML, CSS
from io import BytesIO
from datetime import datetime
import logging
import re
from typing import List, Tuple

logger = logging.getLogger(__name__)


def generate_pdf_report(
    report_content: str,
    candidate_name: str,
    rol_laboral: str,
    nivel_academico: str,
    ciclo_formativo: str,
    duracion: str,
    interview_date: datetime,
    messages: List[object]
) -> BytesIO:
    """Generate a professional PDF report from the interview analysis.
    
    Args:
        report_content: The full interview report text from AI
        candidate_name: Name of the candidate
        rol_laboral: Job role (Junior/Middle/Senior)
        nivel_academico: Academic level
        ciclo_formativo: Specific training cycle (DAW, DAM, etc.)
        duracion: Interview duration (Corta/Media/Larga)
        interview_date: Date of the interview
        
    Returns:
        BytesIO: PDF file in memory
    """
    
    # Sanitize and normalize report content: remove duplicated "DATOS DE LA ENTREVISTA",
    # replace placeholders with real metadata, verify orthography examples against messages,
    # and extract a single employability level to render consistently.
    report_content, detected_level = _sanitize_report(
        report_content,
        interview_date,
        rol_laboral,
        nivel_academico,
        ciclo_formativo,
        duracion,
        messages,
    )
    # Parse remaining sections
    sections = _parse_report_sections(report_content)
    
    # Generate HTML with professional styling
    empleabilidad_html = ""
    if detected_level:
        empleabilidad_html = f'<div class="empleabilidad"><div>Nivel de Empleabilidad</div><div class="empleabilidad-nivel">{detected_level}</div></div>'

    html_content = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Informe de Entrevista Técnica - {candidate_name}</title>
        <style>
            @page {{
                size: A4;
                margin: 2cm;
                @bottom-right {{
                    content: "Página " counter(page) " de " counter(pages);
                    font-size: 10px;
                    color: #666;
                }}
            }}
            body {{
                font-family: 'Arial', 'Helvetica', sans-serif;
                line-height: 1.6;
                color: #333;
                font-size: 11pt;
            }}
            .header {{
                text-align: center;
                border-bottom: 3px solid #2563eb;
                padding-bottom: 20px;
                margin-bottom: 30px;
            }}
            .header h1 {{
                color: #1e40af;
                font-size: 24pt;
                margin: 0 0 10px 0;
            }}
            .header .subtitle {{
                color: #64748b;
                font-size: 12pt;
            }}
            .metadata {{
                background-color: #f1f5f9;
                padding: 15px;
                border-radius: 8px;
                margin-bottom: 25px;
            }}
            .metadata-row {{
                display: flex;
                justify-content: space-between;
                margin-bottom: 8px;
            }}
            .metadata-label {{
                font-weight: bold;
                color: #475569;
            }}
            .metadata-value {{
                color: #1e293b;
            }}
            h2 {{
                color: #1e40af;
                border-bottom: 2px solid #93c5fd;
                padding-bottom: 8px;
                margin-top: 30px;
                margin-bottom: 15px;
                font-size: 16pt;
            }}
            h3 {{
                color: #3b82f6;
                font-size: 13pt;
                margin-top: 20px;
                margin-bottom: 10px;
            }}
            .section {{
                margin-bottom: 25px;
            }}
            .highlight-box {{
                background-color: #dbeafe;
                border-left: 4px solid #2563eb;
                padding: 15px;
                margin: 15px 0;
            }}
            .warning-box {{
                background-color: #fef3c7;
                border-left: 4px solid #f59e0b;
                padding: 15px;
                margin: 15px 0;
            }}
            .success-box {{
                background-color: #d1fae5;
                border-left: 4px solid #10b981;
                padding: 15px;
                margin: 15px 0;
            }}
            ul {{
                margin: 10px 0;
                padding-left: 25px;
            }}
            li {{
                margin-bottom: 8px;
            }}
            .empleabilidad {{
                text-align: center;
                padding: 20px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border-radius: 10px;
                margin: 20px 0;
            }}
            .empleabilidad-nivel {{
                font-size: 28pt;
                font-weight: bold;
                margin: 10px 0;
            }}
            .footer {{
                margin-top: 40px;
                padding-top: 20px;
                border-top: 2px solid #e2e8f0;
                text-align: center;
                font-size: 9pt;
                color: #64748b;
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>Informe de Entrevista Técnica</h1>
            <div class="subtitle">Simulador Evalio - Formación Profesional</div>
        </div>
        
        <div class="metadata">
            <div class="metadata-row">
                <span class="metadata-label">Candidato:</span>
                <span class="metadata-value">{candidate_name}</span>
            </div>
            <div class="metadata-row">
                <span class="metadata-label">Fecha:</span>
                <span class="metadata-value">{interview_date.strftime('%d de %B de %Y')}</span>
            </div>
            <div class="metadata-row">
                <span class="metadata-label">Rol simulado:</span>
                <span class="metadata-value">{rol_laboral}</span>
            </div>
            <div class="metadata-row">
                <span class="metadata-label">Nivel académico:</span>
                <span class="metadata-value">{nivel_academico}</span>
            </div>
            <div class="metadata-row">
                <span class="metadata-label">Ciclo formativo:</span>
                <span class="metadata-value">{ciclo_formativo}</span>
            </div>
            <div class="metadata-row">
                <span class="metadata-label">Duración:</span>
                <span class="metadata-value">{duracion}</span>
            </div>
        </div>
        
        {empleabilidad_html}
        <div class="section">
            {_format_content_to_html(report_content)}
        </div>
        
        <div class="footer">
            <p><strong>Evalio</strong> - Simulador de entrevistas técnicas para Formación Profesional</p>
            <p>Este informe es confidencial y está destinado únicamente al candidato y su centro educativo.</p>
        </div>
    </body>
    </html>
    """
    
    # Generate PDF
    pdf_buffer = BytesIO()
    HTML(string=html_content).write_pdf(pdf_buffer)
    pdf_buffer.seek(0)
    
    logger.info(f"PDF report generated successfully for candidate: {candidate_name}")
    
    return pdf_buffer


def _parse_report_sections(content: str) -> dict:
    """Parse the AI-generated report into structured sections."""
    # Simple parser - could be enhanced based on actual AI output format
    sections = {}
    current_section = "general"
    current_content = []
    
    for line in content.split('\n'):
        line = line.strip()
        if line.startswith('#') or line.endswith(':'):
            if current_content:
                sections[current_section] = '\n'.join(current_content)
            current_section = line.replace('#', '').replace(':', '').strip().lower()
            current_content = []
        else:
            current_content.append(line)
    
    if current_content:
        sections[current_section] = '\n'.join(current_content)
    
    return sections


def _format_content_to_html(content: str) -> str:
    """Convert markdown-like content to HTML with styling."""
    html_parts = []
    lines = content.split('\n')
    in_list = False
    
    for line in lines:
        line = line.strip()
        if not line:
            if in_list:
                html_parts.append('</ul>')
                in_list = False
            html_parts.append('<br>')
            continue
        
        # Headers
        if line.startswith('###'):
            if in_list:
                html_parts.append('</ul>')
                in_list = False
            html_parts.append(f'<h3>{line.replace("###", "").strip()}</h3>')
        elif line.startswith('##'):
            if in_list:
                html_parts.append('</ul>')
                in_list = False
            html_parts.append(f'<h2>{line.replace("##", "").strip()}</h2>')
        elif line.startswith('#'):
            if in_list:
                html_parts.append('</ul>')
                in_list = False
            html_parts.append(f'<h2>{line.replace("#", "").strip()}</h2>')
        
        # Lists
        elif line.startswith('- ') or line.startswith('* '):
            if not in_list:
                html_parts.append('<ul>')
                in_list = True
            html_parts.append(f'<li>{line[2:]}</li>')
        
        # Highlight boxes
        elif 'puntos fuertes' in line.lower() or 'fortalezas' in line.lower():
            if in_list:
                html_parts.append('</ul>')
                in_list = False
            html_parts.append(f'<div class="success-box"><strong>{line}</strong></div>')
        elif 'aspectos a mejorar' in line.lower() or 'debilidades' in line.lower():
            if in_list:
                html_parts.append('</ul>')
                in_list = False
            html_parts.append(f'<div class="warning-box"><strong>{line}</strong></div>')
        elif 'empleabilidad' in line.lower():
            if in_list:
                html_parts.append('</ul>')
                in_list = False
            # Skip inline empleabilidad blocks here — banner is rendered independently
            # to ensure consistency. Do not render anything for these lines.
            continue
        
        # Regular paragraph
        else:
            if in_list:
                html_parts.append('</ul>')
                in_list = False
            # Bold text
            line = line.replace('**', '<strong>').replace('**', '</strong>')
            html_parts.append(f'<p>{line}</p>')
    
    if in_list:
        html_parts.append('</ul>')
    
    return '\n'.join(html_parts)


def _sanitize_report(content: str, interview_date: datetime, rol: str, nivel: str, ciclo: str, duracion: str, messages: List[object]):
    """Clean and normalize AI report content.
    Returns tuple (cleaned_content, detected_level)
    - Removes "DATOS DE LA ENTREVISTA" section (already in header)
    - Removes JSON blocks
    - Removes metadata bullet points
    - Replaces placeholders with real values
    - Extracts employability level
    - Verifies orthography examples
    """
    text = content or ""
    text = text.replace('\r\n', '\n')

    # REMOVE COMPLETE "DATOS DE LA ENTREVISTA" SECTION (with various formatting)
    # This is very aggressive to catch all variations
    # Match: heading (with any # count) + "DATOS DE LA ENTREVISTA" + everything until next heading or metadata block
    text = re.sub(
        r'(?mi)^#+\s*DATOS\s+DE\s+LA\s+ENTREVISTA\s*:?.*?(?=\n#+\s+[A-Z]|\n\n[A-Z]|\Z)',
        '',
        text,
        flags=re.MULTILINE | re.DOTALL
    )
    
    # Also catch bullet-point style "DATOS DE LA ENTREVISTA" sections (common from AI)
    text = re.sub(
        r'(?mi)DATOS\s+DE\s+LA\s+ENTREVISTA\s*:?\s*\n(\s*[-•*]\s*[^\n]*\n)+',
        '',
        text
    )
    
    # Remove metadata bullet points (duplicates from data that should only be in header)
    # This regex catches any line that starts with bullet and contains metadata keys
    meta_keys = ['candidato', 'fecha', 'rol simulado', 'nivel académico', 'ciclo formativo', 'duración']
    
    lines = text.split('\n')
    cleaned = []
    
    for ln in lines:
        l_lower = ln.strip().lower()
        
        # Skip lines that are clearly metadata (start with bullet and contain metadata info)
        if (l_lower.startswith('-') or l_lower.startswith('•') or l_lower.startswith('*')) and any(key in l_lower for key in meta_keys):
            continue
        
        # Skip standalone metadata rows (no bullets, just "Key: value" format at document start)
        if ':' in ln and len(ln) < 120 and any(key in l_lower for key in meta_keys):
            # But only skip if it looks like metadata (e.g., "Candidato: hugo" or "Fecha: 15 de January...")
            # not if it's part of a larger narrative
            key_part = l_lower.split(':')[0].strip()
            if any(key in key_part for key in meta_keys):
                continue
        
        cleaned.append(ln)
    
    text = '\n'.join(cleaned)

    # REMOVE JSON BLOCKS if they exist
    text = re.sub(r'(?ms)---JSON-REPORT-START---.*?---JSON-REPORT-END---', '', text)
    text = re.sub(r'(?ms)```json.*?```', '', text)

    # Replace common placeholders with real values
    date_str = interview_date.strftime('%d de %B de %Y') if interview_date else 'Fecha no especificada'
    placeholder_map = {
        '[fecha real de la entrevista]': date_str,
        '[fecha actual]': date_str,
        '[fecha]': date_str,
        '[rol proporcionado por el candidato]': rol,
        '[rol laboral simulado]': rol,
        '[rol]': rol,
        '[nivel académico proporcionado por el candidato]': nivel,
        '[nivel académico]': nivel,
        '[nivel]': nivel,
        '[nombre específico del ciclo proporcionado por el candidato]': ciclo,
        '[ciclo formativo]': ciclo,
        '[ciclo]': ciclo,
        '[duración proporcionada por el candidato]': duracion,
        '[duración configurada]': duracion,
        '[duración]': duracion,
    }
    for k, v in placeholder_map.items():
        text = re.sub(re.escape(k), v or 'No especificado', text, flags=re.IGNORECASE)

    # Extract employability level
    detected_level = ''
    # First try to find explicit "Nivel de Empleabilidad: ..." pattern
    m = re.search(
        r'Nivel\s+(?:de\s+)?Empleabilidad[:\-\s]+([A-Za-z\s]+?)(?:\n|$)',
        text,
        re.IGNORECASE
    )
    if m:
        level_text = m.group(1).strip().lower()
        for valid_level in ['muy bajo', 'bajo', 'medio', 'bueno', 'muy bueno']:
            if valid_level in level_text:
                detected_level = valid_level.title() if valid_level != 'muy bajo' and valid_level != 'muy bueno' else valid_level
                break
    
    # If not found, search for level keyword anywhere in text
    if not detected_level:
        for valid_level in ['muy bajo', 'bajo', 'medio', 'bueno', 'muy bueno']:
            if re.search(r'\b' + re.escape(valid_level) + r'\b', text, re.IGNORECASE):
                detected_level = valid_level.title() if valid_level != 'muy bajo' and valid_level != 'muy bueno' else valid_level
                break

    # Remove inline "Nivel de Empleabilidad" mentions (will be rendered as banner)
    text = re.sub(r'(?mi)^[#]*\s*Nivel\s+(?:de\s+)?Empleabilidad.*?(?=\n#|\n\n|\Z)', '', text)
    text = re.sub(r'(?mi)^\*\*Nivel\s+(?:de\s+)?Empleabilidad.*$', '', text, flags=re.MULTILINE)

    # Verify orthography examples near 'Ejemplos' or 'Ortografía'
    low = text.lower()
    idx = max(low.rfind('ejempl'), low.rfind('ortograf'))  # Use last occurrence
    if idx != -1:
        frag_end = min(len(text), idx + 1000)
        frag = text[idx:frag_end]
        quoted = re.findall(r'"([^\"]+)"', frag)
        verified = []
        
        for q in quoted:
            ql = q.strip().lower()
            # Skip very short quotes (likely not real spelling errors)
            if len(ql) < 2:
                continue
            
            present = False
            for msg in messages:
                try:
                    msg_content = (msg.contenido or '').lower() if hasattr(msg, 'contenido') else (msg.get('contenido', '') or '').lower()
                    # More flexible matching: check if the word appears in the message
                    # Allow for minor variations (case, punctuation)
                    if ql in msg_content or any(ql in word.lower() for word in msg_content.split()):
                        present = True
                        break
                except Exception:
                    pass
            if present:
                verified.append(q)
        
        # If no examples were verified but quotes exist, it's likely the AI saying "no errors"
        # Check if the fragment contains phrases indicating no errors
        no_errors_phrases = [
            'no se detectaron',
            'no hubo',
            'sin errores',
            'no presenta faltas',
            'correcta expresión',
            'buena ortografía'
        ]
        has_no_error_statement = any(phrase in frag.lower() for phrase in no_errors_phrases)
        
        # Only remove unverified examples if there are actual error reports (not "no errors" statements)
        if quoted and not has_no_error_statement:
            new_frag = frag
            for q in quoted:
                if q not in verified:
                    # Remove the line containing the unverified example
                    new_frag = re.sub(r'[^\n]*"' + re.escape(q) + r'"[^\n]*\n?', '', new_frag)
            text = text[:idx] + new_frag + text[frag_end:]

    # Remove remaining bracket placeholders
    text = re.sub(r'\[.*?\]', '', text)
    
    # Clean up multiple blank lines
    text = re.sub(r'\n\n\n+', '\n\n', text)
    
    return text.strip(), detected_level
