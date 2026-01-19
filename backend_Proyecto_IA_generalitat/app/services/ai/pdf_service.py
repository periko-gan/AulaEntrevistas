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
    """Basic sanitization of AI report content.
    Returns tuple (cleaned_content, detected_level)
    """
    text = content or ""
    text = text.replace('\r\n', '\n')

    # Remove duplicated metadata bullets
    lines = text.split('\n')
    cleaned = []
    meta_keys = ['fecha de la entrevista', 'rol laboral simulado', 'nivel académico', 'ciclo formativo', 'duración configurada', 'duración:']
    for ln in lines:
        l = ln.strip().lower()
        if (l.startswith('-') or l.startswith('•') or l.startswith('*')) and any(k in l for k in meta_keys):
            continue
        cleaned.append(ln)
    text = '\n'.join(cleaned)

    # Replace common placeholders
    date_str = interview_date.strftime('%d de %B de %Y') if interview_date else ''
    placeholder_map = {
        '[fecha real de la entrevista]': date_str,
        '[fecha actual]': date_str,
        '[rol proporcionado por el candidato]': rol,
        '[nivel académico proporcionado por el candidato]': nivel,
        '[nombre específico del ciclo proporcionado por el candidato]': ciclo,
        '[duración proporcionada por el candidato]': duracion,
        '[duración configurada]': duracion,
    }
    for k, v in placeholder_map.items():
        text = re.sub(re.escape(k), v or '', text, flags=re.IGNORECASE)

    # Extract employability level (if present)
    detected_level = ''
    m = re.search(r'Nivel\s*(?:de\s*)?Empleabilidad[:\-\s]*\s*(muy bajo|bajo|medio|bueno|muy bueno)', text, flags=re.IGNORECASE)
    if m:
        detected_level = m.group(1).strip().title()
    else:
        m2 = re.search(r'\b(muy bajo|bajo|medio|bueno|muy bueno)\b', text, flags=re.IGNORECASE)
        if m2:
            detected_level = m2.group(1).strip().title()

    # Remove inline employability blocks to avoid duplicates
    text = re.sub(r'(?mi)^.*nivel\s*(?:de\s*)?empleabilidad.*$', '', text)
    text = re.sub(r'(?mi)\*\*(muy bajo|bajo|medio|bueno|muy bueno)\*\*:\s*.*$', '', text)

    # Verify orthography examples near 'Ejemplos' or 'Ortografía'
    low = text.lower()
    idx = low.find('ejempl')
    if idx == -1:
        idx = low.find('ortograf')
    if idx != -1:
        frag_end = min(len(text), idx + 800)
        frag = text[idx:frag_end]
        quoted = re.findall(r'"([^\"]+)"', frag)
        verified = []
        for q in quoted:
            ql = q.strip().lower()
            present = False
            for msg in messages:
                try:
                    if ql in (msg.contenido or '').lower():
                        present = True
                        break
                except Exception:
                    if isinstance(msg, dict) and ql in (msg.get('contenido','') or '').lower():
                        present = True
                        break
            if present:
                verified.append(q)
        # rebuild fragment with only verified examples
        if quoted:
            new_frag = frag
            for q in quoted:
                if q not in verified:
                    new_frag = re.sub(r'[^\n]*"' + re.escape(q) + r'"[^\n]*\n?', '', new_frag)
            # replace original fragment
            text = text[:idx] + new_frag + text[frag_end:]
            # update counts placeholders if any
            text = re.sub(r'\[número de faltas\]', str(len(verified)), text, flags=re.IGNORECASE)

    # Strip leftover bracket placeholders
    text = re.sub(r'\[.*?\]', '', text)

    return text.strip(), detected_level
