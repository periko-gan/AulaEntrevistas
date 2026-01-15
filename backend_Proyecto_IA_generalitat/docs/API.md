# API Documentation - Backend Proyecto IA Generalitat

## Índice
- [Autenticación](#autenticación)
- [Usuarios](#usuarios)
- [Chats](#chats)
- [Mensajes](#mensajes)
- [IA - Interacción](#ia---interacción)
- [Rate Limiting](#rate-limiting)
- [Códigos de Error](#códigos-de-error)

## Base URL
```
http://localhost:8000/api/v1
```

## Autenticación

Todos los endpoints (excepto `/auth/register` y `/auth/login`) requieren un JWT token en el header:

```
Authorization: Bearer <token>
```

### POST /auth/register

Registrar un nuevo usuario.

**Request:**
```json
{
  "email": "usuario@example.com",
  "password": "Password123",
  "nombre": "Juan Pérez"
}
```

**Validaciones:**
- `email`: Debe ser un email válido
- `password`: Mínimo 8 caracteres, debe contener letras y números
- `nombre`: Solo letras y espacios

**Response:** `201 Created`
```json
{
  "id": 1,
  "email": "usuario@example.com",
  "nombre": "Juan Pérez",
  "created_at": "2024-01-15T10:30:00+02:00"
}
```

**Errores:**
- `400`: Email ya registrado
- `422`: Datos de validación incorrectos

---

### POST /auth/login

Iniciar sesión y obtener token JWT.

**Request:**
```json
{
  "email": "usuario@example.com",
  "password": "Password123"
}
```

**Response:** `200 OK`
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Errores:**
- `401`: Credenciales incorrectas

---

### GET /auth/me

Obtener información del usuario autenticado.

**Headers:** `Authorization: Bearer <token>`

**Response:** `200 OK`
```json
{
  "id": 1,
  "email": "usuario@example.com",
  "nombre": "Juan Pérez",
  "created_at": "2024-01-15T10:30:00+02:00"
}
```

---

## Chats

### POST /chats

Crear un nuevo chat.

**Headers:** `Authorization: Bearer <token>`

**Request:**
```json
{
  "title": "Entrevista de Desarrollo Web"
}
```

**Validaciones:**
- `title`: Entre 1-200 caracteres, no solo espacios

**Response:** `201 Created`
```json
{
  "id": 1,
  "user_id": 1,
  "title": "Entrevista de Desarrollo Web",
  "status": "active",
  "created_at": "2024-01-15T10:30:00+02:00",
  "updated_at": "2024-01-15T10:30:00+02:00",
  "completed_at": null
}
```

---

### GET /chats

Listar todos los chats del usuario autenticado.

**Headers:** `Authorization: Bearer <token>`

**Query Parameters:**
- `skip` (opcional): Número de registros a saltar (default: 0)
- `limit` (opcional): Número máximo de registros (default: 100)

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "user_id": 1,
    "title": "Entrevista de Desarrollo Web",
    "status": "active",
    "created_at": "2024-01-15T10:30:00+02:00",
    "updated_at": "2024-01-15T10:30:00+02:00",
    "completed_at": null
  },
  {
    "id": 2,
    "user_id": 1,
    "title": "Entrevista de Marketing",
    "status": "completed",
    "created_at": "2024-01-14T09:00:00+02:00",
    "updated_at": "2024-01-14T09:45:00+02:00",
    "completed_at": "2024-01-14T09:45:00+02:00"
  }
]
```

---

### GET /chats/{chat_id}

Obtener un chat específico con sus mensajes.

**Headers:** `Authorization: Bearer <token>`

**Response:** `200 OK`
```json
{
  "id": 1,
  "user_id": 1,
  "title": "Entrevista de Desarrollo Web",
  "status": "active",
  "created_at": "2024-01-15T10:30:00+02:00",
  "updated_at": "2024-01-15T10:30:00+02:00",
  "completed_at": null,
  "messages": [
    {
      "id": 1,
      "chat_id": 1,
      "content": "Hola, soy Evalio...",
      "role": "assistant",
      "created_at": "2024-01-15T10:31:00+02:00"
    }
  ]
}
```

**Errores:**
- `404`: Chat no encontrado
- `403`: Chat pertenece a otro usuario

---

### PUT /chats/{chat_id}/title

Actualizar el título de un chat.

**Headers:** `Authorization: Bearer <token>`

**Request:**
```json
{
  "title": "Nuevo Título"
}
```

**Response:** `200 OK`
```json
{
  "id": 1,
  "user_id": 1,
  "title": "Nuevo Título",
  "status": "active",
  "created_at": "2024-01-15T10:30:00+02:00",
  "updated_at": "2024-01-15T11:00:00+02:00",
  "completed_at": null
}
```

**Errores:**
- `404`: Chat no encontrado
- `403`: Chat pertenece a otro usuario
- `422`: Título inválido

---

### DELETE /chats/{chat_id}

Eliminar un chat y todos sus mensajes.

**Headers:** `Authorization: Bearer <token>`

**Response:** `204 No Content`

**Errores:**
- `404`: Chat no encontrado
- `403`: Chat pertenece a otro usuario

---

## Mensajes

### GET /chats/{chat_id}/messages

Obtener todos los mensajes de un chat.

**Headers:** `Authorization: Bearer <token>`

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "chat_id": 1,
    "content": "Hola, soy Evalio...",
    "role": "assistant",
    "created_at": "2024-01-15T10:31:00+02:00"
  },
  {
    "id": 2,
    "chat_id": 1,
    "content": "empezar",
    "role": "user",
    "created_at": "2024-01-15T10:32:00+02:00"
  }
]
```

---

### POST /chats/{chat_id}/messages

Crear un mensaje en un chat (uso interno, ver endpoint `/ai/reply`).

---

## IA - Interacción

### POST /ai/initialize

**Rate Limit:** 100 requests/min

Inicializar un chat con el mensaje de presentación de Evalio.

**Headers:** `Authorization: Bearer <token>`

**Request:**
```json
{
  "chat_id": 1
}
```

**Response:** `200 OK`
```json
{
  "message": "¡Hola! Soy Evalio, tu asistente de evaluación de empleabilidad...",
  "chat_id": 1
}
```

**Errores:**
- `404`: Chat no encontrado
- `403`: Chat pertenece a otro usuario
- `400`: Chat ya completado

---

### POST /ai/reply

**Rate Limit:** 15 requests/min

Enviar un mensaje al chat y recibir respuesta de la IA.

**Headers:** `Authorization: Bearer <token>`

**Request:**
```json
{
  "chat_id": 1,
  "content": "empezar"
}
```

**Response:** `200 OK`
```json
{
  "response": "Perfecto. Para comenzar necesito hacerte 4 preguntas...",
  "chat_id": 1
}
```

**Flujo de la conversación:**
1. Usuario dice "empezar"
2. IA pide 4 datos: Provincia, Municipio, Centro Educativo, Título
3. IA valida que los datos sean correctos
4. IA realiza entrevista de empleabilidad
5. Usuario dice "finalizar"

**Errores:**
- `404`: Chat no encontrado
- `403`: Chat pertenece a otro usuario
- `400`: Chat ya completado
- `429`: Demasiadas peticiones (rate limit)
- `503`: Error de AWS Bedrock

---

### POST /ai/generate-report

**Rate Limit:** 3 requests/hour

Generar reporte PDF de la entrevista. Solo disponible para chats con status 'active' que contengan conversación completa.

**Headers:** `Authorization: Bearer <token>`

**Request:**
```json
{
  "chat_id": 1
}
```

**Response:** `200 OK`
```
Content-Type: application/pdf
Content-Disposition: attachment; filename="reporte_entrevista_1.pdf"

[PDF binary data]
```

**Efectos:**
- Marca el chat con `status='completed'`
- Establece `completed_at` con timestamp actual
- El chat no puede recibir más mensajes

**Errores:**
- `404`: Chat no encontrado
- `403`: Chat pertenece a otro usuario
- `400`: Chat ya completado o sin conversación suficiente
- `429`: Demasiadas peticiones (rate limit)

---

## Rate Limiting

El backend implementa rate limiting en endpoints críticos:

| Endpoint | Límite |
|----------|--------|
| `/ai/reply` | 15 requests/minuto |
| `/ai/generate-report` | 3 requests/hora |
| General | 100 requests/minuto |

**Response cuando se excede:** `429 Too Many Requests`
```json
{
  "detail": "Rate limit exceeded: 15 per 1 minute"
}
```

Headers de respuesta:
```
X-RateLimit-Limit: 15
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1705315200
```

---

## Códigos de Error

### 400 Bad Request
Petición malformada o datos inválidos.
```json
{
  "detail": "El chat ya está completado"
}
```

### 401 Unauthorized
Token JWT inválido o expirado.
```json
{
  "detail": "Could not validate credentials"
}
```

### 403 Forbidden
Acceso denegado (ej: intentar acceder al chat de otro usuario).
```json
{
  "detail": "No tienes permiso para acceder a este chat"
}
```

### 404 Not Found
Recurso no encontrado.
```json
{
  "detail": "Chat no encontrado"
}
```

### 422 Unprocessable Entity
Error de validación de datos.
```json
{
  "detail": [
    {
      "type": "string_too_short",
      "loc": ["body", "password"],
      "msg": "String should have at least 8 characters",
      "input": "pass",
      "ctx": {"min_length": 8}
    }
  ]
}
```

### 429 Too Many Requests
Rate limit excedido.
```json
{
  "detail": "Rate limit exceeded: 15 per 1 minute"
}
```

### 500 Internal Server Error
Error no controlado del servidor.
```json
{
  "detail": "Error interno del servidor",
  "request_id": "abc123"
}
```

### 503 Service Unavailable
Servicio externo no disponible (ej: AWS Bedrock, Database).
```json
{
  "detail": "Database connection error"
}
```

---

## Health Check

### GET /health

Verificar estado de la API, base de datos y AWS.

**Response:** `200 OK`
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00+02:00",
  "database": "ok",
  "aws": "ok"
}
```

**Response (degradado):** `503 Service Unavailable`
```json
{
  "status": "unhealthy",
  "timestamp": "2024-01-15T10:30:00+02:00",
  "database": "error",
  "aws": "degraded"
}
```

---

## Swagger UI

Documentación interactiva disponible en:
```
http://localhost:8000/docs
```

ReDoc disponible en:
```
http://localhost:8000/redoc
```
