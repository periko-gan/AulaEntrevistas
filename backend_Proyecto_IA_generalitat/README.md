# Backend - Proyecto IA Generalitat

Backend FastAPI para sistema de evaluación de empleabilidad con IA (Evalio), desarrollado para la Generalitat.

## 🚀 Características

- **API RESTful** con FastAPI 0.115.0
- **Autenticación JWT** con tokens seguros
- **IA Conversacional** con AWS Bedrock (Amazon Nova)
- **Generación de PDFs** profesionales con WeasyPrint
- **Rate Limiting** para protección de endpoints críticos
- **Testing** con pytest e in-memory database
- **Migraciones** automatizadas con Alembic
- **Docker** para despliegue simplificado
- **Validación robusta** con Pydantic 2.9
- **Exception handling global** para respuestas consistentes

## 📋 Requisitos

- Python 3.11+
- MySQL 8.0
- Docker & Docker Compose (opcional pero recomendado)
- AWS Account con acceso a Bedrock

## 🏃 Quick Start

### Con Docker (Recomendado)

```bash
# 1. Clonar y configurar
git clone <repository-url>
cd backend_Proyecto_IA_generalitat
cp .env.example .env

# 2. Editar .env con tus credenciales
# (ver .env.example para detalles)

# 3. Levantar servicios
docker-compose up --build

# 4. Aplicar migraciones (en otro terminal)
docker-compose exec backend alembic upgrade head

# 5. Verificar
curl http://localhost:8000/health
```

La API estará disponible en:
- **API:** http://localhost:8000
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

### Sin Docker

```bash
# 1. Crear virtual environment
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Configurar .env
cp .env.example .env
# Editar .env con tus valores

# 4. Aplicar migraciones
alembic upgrade head

# 5. Ejecutar
uvicorn app.main:app --reload
```

## 📚 Documentación

- **[API Reference](docs/API.md)** - Documentación completa de endpoints
- **[Arquitectura](docs/ARCHITECTURE.md)** - Diseño y estructura del proyecto
- **[Deployment](docs/DEPLOYMENT.md)** - Guía de despliegue detallada
- **[Testing](tests/README.md)** - Guía de testing
- **[Migraciones](alembic/README.md)** - Uso de Alembic

## 🏗️ Arquitectura

```
┌─────────────────┐
│   API Layer     │  FastAPI endpoints
├─────────────────┤
│ Service Layer   │  Lógica de negocio
├─────────────────┤
│Repository Layer │  Acceso a datos
├─────────────────┤
│ Database Layer  │  MySQL + SQLAlchemy
└─────────────────┘
```

### Estructura de Directorios

```
backend_Proyecto_IA_generalitat/
├── app/
│   ├── api/v1/           # Endpoints REST
│   ├── core/             # Config, database, security
│   ├── models/           # SQLAlchemy models
│   ├── schemas/          # Pydantic schemas
│   ├── repositories/     # Data access layer
│   └── services/         # Business logic
├── alembic/              # Database migrations
├── tests/                # Test suite
├── docs/                 # Documentation
├── docker-compose.yml
├── Dockerfile
└── requirements.txt
```

## 🔐 Seguridad

- ✅ **JWT Authentication** con tokens seguros
- ✅ **Bcrypt** para hashing de passwords
- ✅ **Rate Limiting** (15 req/min en IA, 3 PDFs/hora)
- ✅ **Input Validation** con Pydantic (EmailStr, regex patterns)
- ✅ **Exception Handling** global sin exponer detalles técnicos
- ✅ **Anti Prompt Injection** en system prompt de IA
- ✅ **Secrets Validation** (JWT secret mínimo 32 chars)

## 🧪 Testing

```bash
# Instalar dependencias de testing
pip install -r requirements-dev.txt

# Ejecutar todos los tests
pytest tests/ -v

# Con coverage
pytest tests/ --cov=app --cov-report=html

# Tests específicos
pytest tests/test_auth.py -v
```

**Cobertura actual:**
- ✅ Autenticación (registro, login, validaciones)
- ✅ Chats CRUD
- ✅ Health check
- 🔄 Mensajes (pendiente)
- 🔄 IA endpoints (pendiente)

## 📊 API Endpoints

### Autenticación
- `POST /api/v1/auth/register` - Registrar usuario
- `POST /api/v1/auth/login` - Iniciar sesión
- `GET /api/v1/auth/me` - Info usuario actual

### Chats
- `POST /api/v1/chats` - Crear chat
- `GET /api/v1/chats` - Listar chats
- `GET /api/v1/chats/{id}` - Obtener chat con mensajes
- `PUT /api/v1/chats/{id}/title` - Actualizar título
- `DELETE /api/v1/chats/{id}` - Eliminar chat

### IA
- `POST /api/v1/ai/initialize` - Presentación de Evalio
- `POST /api/v1/ai/reply` - Interactuar con IA (Rate limit: 15/min)
- `POST /api/v1/ai/generate-report` - Generar PDF (Rate limit: 3/hora)

### Monitoreo
- `GET /health` - Health check (API, DB, AWS)

Ver [API.md](docs/API.md) para documentación completa.

## 🚦 Rate Limiting

| Endpoint | Límite |
|----------|--------|
| `/api/v1/ai/reply` | 15 requests/min |
| `/api/v1/ai/generate-report` | 3 requests/hora |
| General | 100 requests/min |

## 🗄️ Migraciones

```bash
# Ver estado actual
alembic current

# Aplicar migraciones
alembic upgrade head

# Crear nueva migración
alembic revision --autogenerate -m "descripcion"

# Revertir última migración
alembic downgrade -1
```

Ver [alembic/README.md](alembic/README.md) para más detalles.

## 🛠️ Desarrollo

### Variables de Entorno

Copia `.env.example` y configura:

```bash
# Database
DATABASE_URL=mysql+pymysql://user:password@localhost:3306/proyecto_ia
TIMEZONE=+02:00

# JWT (CRÍTICO: mínimo 32 caracteres)
JWT_SECRET=tu_secreto_super_seguro_de_al_menos_32_caracteres
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_DAYS=30

# AWS Bedrock
AWS_ACCESS_KEY_ID=tu_access_key
AWS_SECRET_ACCESS_KEY=tu_secret_key
AWS_REGION=us-east-1
BEDROCK_MODEL_ID=us.amazon.nova-micro-v1:0
```

### Instalar Dependencias de Desarrollo

```bash
pip install -r requirements-dev.txt
```

Incluye:
- pytest 7.4.3
- httpx 0.25.2
- faker 20.1.0

### Ejecutar en Modo Desarrollo

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 📦 Dependencias Principales

- **FastAPI** 0.115.0 - Framework web
- **SQLAlchemy** 2.0.34 - ORM
- **Pydantic** 2.9.2 - Validación de datos
- **python-jose** 3.3.0 - JWT tokens
- **bcrypt** 4.0.1 - Password hashing
- **boto3** 1.35.0 - AWS SDK
- **WeasyPrint** 62.3 - Generación de PDFs
- **slowapi** 0.1.9 - Rate limiting
- **alembic** 1.13.1 - Migraciones

Ver [requirements.txt](requirements.txt) para lista completa.

## 🐛 Troubleshooting

### Error: "Could not connect to database"
```bash
# Verificar que MySQL esté corriendo
docker-compose ps

# Ver logs
docker-compose logs db
```

### Error: "AWS credentials not found"
```bash
# Verificar variables en .env
cat .env | grep AWS
```

### Error: "Rate limit exceeded"
Esperar reset del límite o ajustar configuración en desarrollo.

Ver [DEPLOYMENT.md](docs/DEPLOYMENT.md) para más soluciones.

## 📈 Próximas Mejoras

### Implementado ✅
- Exception handling global
- Input validation completa
- Rate limiting
- Testing infrastructure
- Alembic para migraciones
- Health check mejorado
- Documentación completa

### Pendiente 🔄
- Async file I/O para PDFs
- Caché con Redis
- Websockets para chat en tiempo real
- CORS configurado (requiere dominio)
- Celery para PDFs asíncronos
- S3 para almacenamiento de PDFs
- CI/CD pipeline

## 📄 Licencia

Ver [LICENSE.txt](../LICENSE.txt)

## 🤝 Contribuir

1. Fork el proyecto
2. Crear feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a branch (`git push origin feature/AmazingFeature`)
5. Abrir Pull Request

### Convenciones de Código

- **Naming:** snake_case para funciones/variables, PascalCase para clases
- **Type hints:** Obligatorio en todas las funciones
- **Docstrings:** Para funciones públicas
- **Tests:** Escribir tests para nuevas features

## 📞 Contacto

Para bugs o features, crear issue en el repositorio.

---

**Última actualización:** Enero 2026
