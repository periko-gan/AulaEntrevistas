from weasyprint import HTML, CSS
from io import BytesIO
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


def generate_pdf_report(
    report_content: str,
    candidate_name: str,
    rol_laboral: str,
    nivel_academico: str,
    ciclo_formativo: str,
    duracion: str,
    interview_date: datetime
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
    
    # Parse report content sections
    sections = _parse_report_sections(report_content)
    
    # Generate HTML with professional styling
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
            <h1>📋 Informe de Entrevista Técnica</h1>
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
            # Extract nivel - ahora con 5 niveles
            nivel = 'Medio'
            if 'muy bajo' in line.lower():
                nivel = 'Muy Bajo'
            elif 'bajo' in line.lower():
                nivel = 'Bajo'
            elif 'muy bueno' in line.lower() or 'muy alto' in line.lower():
                nivel = 'Muy Bueno'
            elif 'bueno' in line.lower() or 'alto' in line.lower():
                nivel = 'Bueno'
            elif 'medio' in line.lower():
                nivel = 'Medio'
            html_parts.append(f'<div class="empleabilidad"><div>Nivel de Empleabilidad</div><div class="empleabilidad-nivel">{nivel}</div></div>')
        
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
