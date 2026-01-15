# Endpoint de Generación de PDF - Informe de Entrevista

## Endpoint
```
POST /api/v1/ai/generate-report
```

## Autenticación
Requiere token JWT en el header `Authorization: Bearer <token>`

## Request Body
```json
{
  "chat_id": 123
}
```

## Respuesta
Devuelve un archivo PDF como descarga directa con:
- **Content-Type**: `application/pdf`
- **Content-Disposition**: `attachment; filename=informe_entrevista_{chat_id}_{fecha}.pdf`

## Flujo del Endpoint

1. **Validación**: Verifica que el chat pertenece al usuario autenticado
2. **Historial**: Recupera todos los mensajes del chat (hasta 100)
3. **Generación del informe**: 
   - Envía prompt especial a la IA pidiendo el informe final
   - La IA genera el informe siguiendo el formato del system_prompt
   - Max tokens: 2500 (para informe completo)
4. **Extracción de metadata**: 
   - Analiza los mensajes para detectar rol, nivel académico y área
   - Si no encuentra los datos, usa "No especificado"
5. **Generación de PDF**:
   - Convierte el informe a HTML con diseño profesional
   - Genera PDF con WeasyPrint
   - Incluye header, metadata, secciones formateadas y footer
6. **Descarga**: Devuelve el PDF como streaming response

## Ejemplo de uso (Frontend)

```javascript
const generarPDF = async (chatId) => {
  try {
    const token = localStorage.getItem('token');
    
    const response = await fetch('/api/v1/ai/generate-report', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({ chat_id: chatId })
    });
    
    if (!response.ok) {
      throw new Error('Error generando el informe');
    }
    
    // Convertir respuesta a blob
    const blob = await response.blob();
    
    // Crear URL temporal y descargar
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `informe_entrevista_${chatId}.pdf`;
    document.body.appendChild(a);
    a.click();
    
    // Limpiar
    window.URL.revokeObjectURL(url);
    document.body.removeChild(a);
    
    console.log('PDF generado y descargado correctamente');
  } catch (error) {
    console.error('Error:', error);
    alert('No se pudo generar el informe PDF');
  }
};

// Usar en un botón
<button onClick={() => generarPDF(123)}>
  Descargar Informe PDF
</button>
```

## Diseño del PDF

El PDF incluye:

### Header
- Título: "📋 Informe de Entrevista Técnica"
- Subtítulo: "Simulador Evalio - Formación Profesional"

### Metadata Box (destacado)
- Nombre del candidato
- Fecha de la entrevista
- Rol laboral simulado
- Nivel académico
- Área principal

### Contenido del Informe
Formateado automáticamente con:
- **Headers H2/H3**: Con líneas separadoras azules
- **Listas**: Con viñetas y espaciado
- **Cajas destacadas**:
  - Verde: Puntos fuertes
  - Amarillo: Aspectos a mejorar
  - Azul: Información general
- **Empleabilidad**: Caja especial con gradiente morado

### Footer
- Texto informativo sobre Evalio
- Nota de confidencialidad

## Notas Técnicas

- **Librería**: WeasyPrint (convierte HTML a PDF)
- **Paginación**: Automática con contador de páginas
- **Tamaño**: A4
- **Márgenes**: 2cm en todos los lados
- **Fuente**: Arial/Helvetica (profesional y clara)

## Errores Posibles

- `404`: Chat no encontrado o no pertenece al usuario
- `400`: Error de validación (ej: input injection detectado)
- `500`: Error generando el informe o el PDF

## Instalación de Dependencias

Añadir a `requirements.txt`:
```
weasyprint==62.3
```

Y reinstalar:
```bash
docker-compose down
docker-compose build
docker-compose up
```
