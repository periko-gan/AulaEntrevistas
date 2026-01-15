# Arquitectura del Backend

## Visión General

El backend está construido con **FastAPI** siguiendo una arquitectura en capas que separa responsabilidades:

```
┌─────────────────────────────────────────────┐
│           API Layer (FastAPI)               │
│  /api/v1/auth, /chats, /messages, /ai      │
└─────────────────┬───────────────────────────┘
                  │
┌─────────────────▼───────────────────────────┐
│         Service Layer (Business Logic)      │
│  auth_service, chat_service, message_service│
│           bedrock_service, pdf_service      │
└─────────────────┬───────────────────────────┘
                  │
┌─────────────────▼───────────────────────────┐
│      Repository Layer (Data Access)         │
│  user_repo, chat_repo, message_repo         │
└─────────────────┬───────────────────────────┘
                  │
┌─────────────────▼───────────────────────────┐
│         Database Layer (SQLAlchemy)         │
│           MySQL 8.0 + Alembic               │
└─────────────────────────────────────────────┘
```

## Estructura de Directorios

```
backend_Proyecto_IA_generalitat/
│
├── app/
│   ├── main.py                    # Punto de entrada, configuración FastAPI
│   │
│   ├── api/                       # Capa de API (Endpoints)
│   │   ├── deps.py               # Dependencias compartidas (get_db, get_current_user)
│   │   └── v1/                   # Versión 1 de la API
│   │       ├── router.py         # Router principal que agrupa rutas
│   │       ├── auth.py           # Endpoints de autenticación
│   │       ├── chats.py          # CRUD de chats
│   │       ├── messages.py       # CRUD de mensajes
│   │       └── ai.py             # Interacción con IA y generación de PDFs
│   │
│   ├── core/                      # Configuración y utilidades core
│   │   ├── config.py             # Settings (variables de entorno)
│   │   ├── database.py           # Configuración de SQLAlchemy
│   │   ├── security.py           # JWT, hashing de passwords
│   │   └── exceptions.py         # Exception handlers globales
│   │
│   ├── models/                    # Modelos SQLAlchemy (DB schema)
│   │   ├── user.py               # Tabla users
│   │   ├── chat.py               # Tabla chats
│   │   └── message.py            # Tabla messages
│   │
│   ├── schemas/                   # Esquemas Pydantic (validación)
│   │   ├── auth.py               # RegisterRequest, LoginRequest, Token
│   │   ├── user.py               # UserResponse, UserCreate
│   │   ├── chat.py               # ChatCreate, ChatResponse, ChatUpdate
│   │   ├── message.py            # MessageCreate, MessageResponse
│   │   └── ai.py                 # AIReplyRequest, AIReplyResponse
│   │
│   ├── repositories/              # Capa de acceso a datos
│   │   ├── user_repo.py          # CRUD de usuarios
│   │   ├── chat_repo.py          # CRUD de chats
│   │   └── message_repo.py       # CRUD de mensajes
│   │
│   └── services/                  # Lógica de negocio
│       ├── auth_service.py       # Registro, login, verificación
│       ├── chat_service.py       # Lógica de chats
│       ├── message_service.py    # Lógica de mensajes
│       └── ai/
│           ├── bedrock_service.py    # Interacción con AWS Bedrock
│           ├── pdf_service.py        # Generación de PDFs
│           └── system_prompt.txt     # Prompt del sistema para Evalio
│
├── alembic/                       # Migraciones de base de datos
│   ├── versions/                 # Scripts de migración
│   ├── env.py                    # Configuración de Alembic
│   └── README.md
│
├── tests/                         # Suite de testing
│   ├── conftest.py               # Fixtures compartidos
│   ├── test_auth.py
│   ├── test_chats.py
│   └── README.md
│
├── docs/                          # Documentación
│   ├── API.md                    # Documentación de endpoints
│   ├── ARCHITECTURE.md           # Este archivo
│   └── DEPLOYMENT.md             # Guía de despliegue
│
├── docker-compose.yml             # Orquestación de contenedores
├── Dockerfile                     # Imagen de Docker
├── requirements.txt               # Dependencias Python
├── requirements-dev.txt           # Dependencias de desarrollo
├── pytest.ini                     # Configuración de pytest
├── alembic.ini                    # Configuración de Alembic
└── .env.example                   # Template de variables de entorno
```

## Capas de la Aplicación

### 1. API Layer (`app/api/`)

**Responsabilidad:** Exponer endpoints HTTP, validar requests, devolver responses.

**Características:**
- Rutas organizadas por versión (`/api/v1/`)
- Dependencias inyectadas (`Depends(get_db)`, `Depends(get_current_user)`)
- Rate limiting en endpoints críticos
- Validación automática vía Pydantic

**Ejemplo:**
```python
# app/api/v1/chats.py
@router.post("/", response_model=ChatResponse, status_code=201)
@limiter.limit("100/minute")
async def create_chat(
    request: Request,
    chat_data: ChatCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return chat_service.create_chat(db, chat_data, current_user.id)
```

### 2. Service Layer (`app/services/`)

**Responsabilidad:** Lógica de negocio, orquestación de repositorios, integración con servicios externos.

**Características:**
- Sin acceso directo a la base de datos (usa repositorios)
- Orquesta múltiples repositorios si es necesario
- Integra servicios externos (AWS Bedrock, WeasyPrint)
- Maneja lógica compleja de negocio

**Ejemplo:**
```python
# app/services/chat_service.py
def create_chat(db: Session, chat_data: ChatCreate, user_id: int) -> Chat:
    # Validar título
    if not chat_data.title.strip():
        raise HTTPException(400, "El título no puede estar vacío")
    
    # Crear chat usando repositorio
    chat = chat_repo.create_chat(db, user_id, chat_data.title)
    
    # Inicializar con mensaje de Evalio (si fuera necesario)
    # ...
    
    return chat
```

### 3. Repository Layer (`app/repositories/`)

**Responsabilidad:** Acceso a datos, queries SQL, operaciones CRUD.

**Características:**
- Única capa que interactúa con SQLAlchemy
- Queries reutilizables
- Abstracción de la base de datos

**Ejemplo:**
```python
# app/repositories/chat_repo.py
def get_chat_by_id(db: Session, chat_id: int) -> Optional[Chat]:
    return db.query(Chat).filter(Chat.id == chat_id).first()

def get_user_chats(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(Chat)\
        .filter(Chat.user_id == user_id)\
        .order_by(Chat.created_at.desc())\
        .offset(skip)\
        .limit(limit)\
        .all()
```

### 4. Models (`app/models/`)

**Responsabilidad:** Definir el schema de la base de datos.

**Características:**
- Clases SQLAlchemy (ORM)
- Relaciones entre tablas
- Índices y constraints

**Ejemplo:**
```python
# app/models/chat.py
class Chat(Base):
    __tablename__ = "chats"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(200), nullable=False)
    status = Column(String(20), default="active", nullable=False, index=True)
    completed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # Relaciones
    user = relationship("User", back_populates="chats")
    messages = relationship("Message", back_populates="chat", cascade="all, delete-orphan")
```

### 5. Schemas (`app/schemas/`)

**Responsabilidad:** Validación de entrada/salida con Pydantic.

**Características:**
- Validación automática de tipos
- Validators personalizados
- Separación entre Request y Response schemas

**Ejemplo:**
```python
# app/schemas/chat.py
class ChatCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    
    @field_validator("title")
    def validate_title(cls, v):
        if not v.strip():
            raise ValueError("El título no puede estar vacío")
        return v.strip()

class ChatResponse(BaseModel):
    id: int
    user_id: int
    title: str
    status: str
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)
```

## Flujo de una Request

```
1. Cliente HTTP
   │
   ▼
2. Middleware (Rate Limiter, Exception Handlers)
   │
   ▼
3. API Endpoint (app/api/v1/chats.py)
   │  - Valida datos (Pydantic)
   │  - Inyecta dependencias (DB session, user autenticado)
   ▼
4. Service Layer (app/services/chat_service.py)
   │  - Lógica de negocio
   │  - Orquesta repositorios
   ▼
5. Repository Layer (app/repositories/chat_repo.py)
   │  - Queries SQL con SQLAlchemy
   ▼
6. Database (MySQL)
   │
   ▼
7. Respuesta sube por las capas
   │  Repository → Service → API
   ▼
8. Serialización JSON (Pydantic)
   │
   ▼
9. Cliente HTTP recibe respuesta
```

## Componentes Externos

### AWS Bedrock (Amazon Nova)
- **Propósito:** IA conversacional para Evalio
- **Servicio:** `bedrock_service.py`
- **Modelo:** `us.amazon.nova-micro-v1:0`
- **Anti Prompt Injection:** Validación de respuestas en system prompt

### WeasyPrint
- **Propósito:** Generación de PDFs profesionales
- **Servicio:** `pdf_service.py`
- **Input:** Texto markdown-like de la conversación
- **Output:** PDF con estilos CSS, gráficas de empleabilidad

### MySQL 8.0
- **Propósito:** Persistencia de datos
- **ORM:** SQLAlchemy 2.0
- **Migraciones:** Alembic
- **Timezone:** Configurable (default: +02:00)

## Seguridad

### Autenticación
- **JWT Tokens** con python-jose
- Algoritmo: HS256
- Expiración: Configurable (default: 30 días)
- Secret: Mínimo 32 caracteres (validado en config.py)

### Passwords
- **bcrypt** para hashing
- Pre-hash con SHA-256 para passwords largos (limitación bcrypt 72 bytes)
- Salt rounds: 12 (default bcrypt)

### Rate Limiting
- **slowapi** (basado en Flask-Limiter)
- Límites por IP
- Configurables por endpoint:
  - `/ai/reply`: 15/min
  - `/ai/generate-report`: 3/hora
  - General: 100/min

### Validación de Inputs
- **Pydantic** para validación de schemas
- `EmailStr` para emails
- Regex para nombres (solo letras y espacios)
- Validación de longitud de strings
- Password strength: mínimo 8 chars, letras + números

### Exception Handling
- Exception handlers globales
- No exponer detalles técnicos al cliente
- Logging de errores con request_id para troubleshooting

## Testing

### Estrategia
- **pytest** como framework
- **httpx** para TestClient de FastAPI
- Base de datos en memoria (SQLite) para tests
- Fixtures compartidos en `conftest.py`

### Cobertura
- ✅ Autenticación (registro, login, validaciones)
- ✅ Chats CRUD
- ✅ Health check
- 🔄 Mensajes (pendiente)
- 🔄 IA endpoints (pendiente)
- 🔄 PDF generation (pendiente)

### Ejecución
```bash
# Todos los tests
pytest tests/ -v

# Tests específicos
pytest tests/test_auth.py -v

# Con coverage
pytest tests/ --cov=app --cov-report=html
```

## Deployment

Ver [DEPLOYMENT.md](DEPLOYMENT.md) para guía completa de despliegue.

### Docker
```bash
docker-compose up --build
```

### Variables de Entorno
Ver `.env.example` para todas las variables necesarias.

### Migraciones
```bash
# Aplicar migraciones
alembic upgrade head

# Crear nueva migración
alembic revision --autogenerate -m "descripcion"
```

## Mejoras Futuras

### Implementado ✅
- Exception handling global
- Input validation completa
- Rate limiting
- Testing infrastructure
- Alembic para migraciones
- Health check mejorado
- .env.example documentado

### Pendiente 🔄
- Async file I/O para PDFs (actualmente síncrono)
- Caché de responses de IA (Redis)
- Websockets para chat en tiempo real
- CORS configurado (requiere dominio)
- Celery para generación asíncrona de PDFs
- S3 para almacenamiento de PDFs
- Monitoring (Prometheus + Grafana)
- CI/CD pipeline

## Convenciones de Código

### Naming
- **Archivos:** snake_case (`chat_service.py`)
- **Clases:** PascalCase (`ChatService`)
- **Funciones/variables:** snake_case (`get_user_chats`)
- **Constants:** UPPER_SNAKE_CASE (`JWT_SECRET`)

### Imports
```python
# Standard library
import os
from typing import Optional

# Third-party
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

# Local
from app.models.chat import Chat
from app.schemas.chat import ChatResponse
```

### Type Hints
Usar type hints en todas las funciones:
```python
def get_chat_by_id(db: Session, chat_id: int) -> Optional[Chat]:
    ...
```

## Referencias

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy 2.0 Documentation](https://docs.sqlalchemy.org/en/20/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [AWS Bedrock Documentation](https://docs.aws.amazon.com/bedrock/)
