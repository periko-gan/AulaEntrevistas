# Guía de Despliegue - Backend Proyecto IA Generalitat

## Requisitos Previos

### Software Necesario
- Docker 20.10+
- Docker Compose 2.0+
- Git

### Servicios Externos
- AWS Account con acceso a Bedrock
- MySQL 8.0 (o usar el contenedor incluido)

---

## Despliegue con Docker (Recomendado)

### 1. Clonar el Repositorio

```bash
git clone <repository-url>
cd backend_Proyecto_IA_generalitat
```

### 2. Configurar Variables de Entorno

Copia el template y edita con tus valores:

```bash
cp .env.example .env
```

Edita `.env`:

```bash
# Database
DATABASE_URL=mysql+pymysql://user:password@db:3306/proyecto_ia
TIMEZONE=+02:00

# JWT (CRÍTICO: Usa un secreto fuerte)
JWT_SECRET=tu_secreto_super_seguro_de_al_menos_32_caracteres
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_DAYS=30

# AWS Bedrock (NUNCA COMMITEAR ESTO)
AWS_ACCESS_KEY_ID=tu_access_key
AWS_SECRET_ACCESS_KEY=tu_secret_key
AWS_REGION=us-east-1
BEDROCK_MODEL_ID=us.amazon.nova-micro-v1:0
```

**⚠️ IMPORTANTE:** 
- `JWT_SECRET` debe tener mínimo 32 caracteres
- **NUNCA** commitear `.env` al repositorio
- Rotar credenciales AWS regularmente

### 3. Construir y Levantar Contenedores

```bash
docker-compose up --build
```

Esto levantará:
- **Backend FastAPI** en `http://localhost:8000`
- **MySQL 8.0** en `localhost:3306`

### 4. Aplicar Migraciones

En otro terminal (con los contenedores corriendo):

```bash
# Entrar al contenedor del backend
docker-compose exec backend bash

# Aplicar migraciones
alembic upgrade head

# Salir del contenedor
exit
```

### 5. Verificar Despliegue

```bash
curl http://localhost:8000/health
```

Deberías ver:
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00+02:00",
  "database": "ok",
  "aws": "ok"
}
```

---

## Despliegue Manual (Sin Docker)

### 1. Instalar Python 3.11+

```bash
# Verificar versión
python --version  # Debe ser 3.11 o superior
```

### 2. Crear Virtual Environment

```bash
# Crear venv
python -m venv venv

# Activar venv
# En Windows:
venv\Scripts\activate
# En Linux/Mac:
source venv/bin/activate
```

### 3. Instalar Dependencias

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configurar Base de Datos MySQL

Crea la base de datos manualmente:

```sql
CREATE DATABASE proyecto_ia CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'user'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON proyecto_ia.* TO 'user'@'localhost';
FLUSH PRIVILEGES;
```

### 5. Configurar Variables de Entorno

Crea archivo `.env` (ver paso 2 de Docker).

### 6. Aplicar Migraciones

```bash
alembic upgrade head
```

### 7. Ejecutar Backend

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

---

## Configuración de AWS Bedrock

### 1. Crear IAM User

En AWS Console:
1. Ir a **IAM** → **Users** → **Create user**
2. Nombre: `bedrock-api-user`
3. Seleccionar **Programmatic access**

### 2. Asignar Permisos

Adjuntar política personalizada:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "bedrock:InvokeModel",
        "bedrock:InvokeModelWithResponseStream"
      ],
      "Resource": "arn:aws:bedrock:us-east-1::foundation-model/us.amazon.nova-micro-v1:0"
    }
  ]
}
```

### 3. Obtener Credenciales

Descarga las credenciales y añádelas a tu `.env`:

```bash
AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
AWS_REGION=us-east-1
```

### 4. Verificar Acceso

```bash
# Desde el contenedor o terminal con venv activo
python -c "
import boto3
from app.core.config import settings

client = boto3.client(
    'bedrock-runtime',
    aws_access_key_id=settings.aws_access_key_id,
    aws_secret_access_key=settings.aws_secret_access_key,
    region_name=settings.aws_region
)
print('AWS Bedrock client initialized successfully')
"
```

---

## Migraciones de Base de Datos

### Ver Estado Actual

```bash
alembic current
```

### Aplicar Todas las Migraciones

```bash
alembic upgrade head
```

### Revertir Última Migración

```bash
alembic downgrade -1
```

### Crear Nueva Migración

```bash
# Autogenerar desde cambios en models
alembic revision --autogenerate -m "add_new_field_to_user"

# Crear migración vacía (manual)
alembic revision -m "custom_migration"
```

### Ver Historial

```bash
alembic history
```

---

## Testing

### Instalar Dependencias de Testing

```bash
pip install -r requirements-dev.txt
```

### Ejecutar Tests

```bash
# Todos los tests
pytest tests/ -v

# Tests específicos
pytest tests/test_auth.py -v

# Con coverage
pytest tests/ --cov=app --cov-report=html

# Ver reporte de coverage
open htmlcov/index.html  # En Linux/Mac
start htmlcov/index.html # En Windows
```

### Estructura de Tests

```
tests/
├── conftest.py           # Fixtures compartidos
├── test_auth.py          # Tests de autenticación
├── test_chats.py         # Tests de chats
├── test_messages.py      # Tests de mensajes (crear)
└── test_ai.py            # Tests de IA (crear)
```

---

## Monitoreo y Logs

### Ver Logs de Docker

```bash
# Logs del backend
docker-compose logs -f backend

# Logs de la base de datos
docker-compose logs -f db

# Todos los logs
docker-compose logs -f
```

### Health Check

El endpoint `/health` verifica:
- ✅ API activa
- ✅ Conexión a base de datos
- ✅ Cliente AWS inicializado

```bash
curl http://localhost:8000/health
```

Respuesta cuando todo está bien (200 OK):
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00+02:00",
  "database": "ok",
  "aws": "ok"
}
```

Respuesta cuando hay problemas (503 Service Unavailable):
```json
{
  "status": "unhealthy",
  "timestamp": "2024-01-15T10:30:00+02:00",
  "database": "error",
  "aws": "degraded"
}
```

---

## Producción

### Checklist de Seguridad

- [ ] `JWT_SECRET` fuerte (mínimo 32 caracteres aleatorios)
- [ ] `.env` en `.gitignore`
- [ ] Credenciales AWS con permisos mínimos necesarios
- [ ] Rate limiting activado
- [ ] HTTPS habilitado (reverse proxy con Nginx/Traefik)
- [ ] CORS configurado con dominio específico
- [ ] Logs centralizados (ELK, CloudWatch)
- [ ] Backups automáticos de base de datos
- [ ] Monitoring (Prometheus + Grafana)

### Configuración de HTTPS (Nginx)

Ejemplo de configuración Nginx:

```nginx
server {
    listen 443 ssl http2;
    server_name api.example.com;

    ssl_certificate /etc/letsencrypt/live/api.example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/api.example.com/privkey.pem;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Variables de Entorno Adicionales (Producción)

```bash
# Desactivar reload en producción
UVICORN_RELOAD=false

# Workers (2-4 por CPU core)
UVICORN_WORKERS=4

# Logs
LOG_LEVEL=warning

# Rate limiting más estricto
RATE_LIMIT_REPLY=10/minute
RATE_LIMIT_PDF=2/hour
```

### Backup de Base de Datos

```bash
# Backup manual
docker-compose exec db mysqldump -u user -p proyecto_ia > backup_$(date +%Y%m%d_%H%M%S).sql

# Restaurar backup
docker-compose exec -T db mysql -u user -p proyecto_ia < backup_20240115_103000.sql
```

### Actualizar Aplicación

```bash
# 1. Hacer pull de cambios
git pull origin main

# 2. Reconstruir contenedores
docker-compose down
docker-compose up --build -d

# 3. Aplicar migraciones
docker-compose exec backend alembic upgrade head

# 4. Verificar health
curl http://localhost:8000/health
```

---

## Troubleshooting

### Error: "Could not connect to database"

**Causa:** MySQL no está disponible o credenciales incorrectas.

**Solución:**
```bash
# Verificar que MySQL esté corriendo
docker-compose ps

# Ver logs de MySQL
docker-compose logs db

# Verificar DATABASE_URL en .env
```

---

### Error: "AWS credentials not found"

**Causa:** Variables AWS no configuradas o incorrectas.

**Solución:**
```bash
# Verificar variables en .env
cat .env | grep AWS

# Probar credenciales
aws bedrock list-foundation-models --region us-east-1
```

---

### Error: "Rate limit exceeded"

**Causa:** Demasiadas peticiones desde la misma IP.

**Solución:**
- Esperar a que se resetee el límite (ver header `X-RateLimit-Reset`)
- Ajustar límites en `app/main.py` si es desarrollo
- Usar diferentes IPs o autenticarse con diferentes usuarios

---

### Error: "Alembic can't locate revision"

**Causa:** Desincronización entre base de datos y migraciones.

**Solución:**
```bash
# Ver estado actual
alembic current

# Si está vacío, marcar como aplicada la última migración
alembic stamp head

# Si hay conflictos, resetear tabla alembic_version
# (CUIDADO: solo en desarrollo)
docker-compose exec db mysql -u user -p -e "
USE proyecto_ia;
DELETE FROM alembic_version;
"
alembic stamp head
```

---

### Logs no Aparecen

**Solución:**
```bash
# Agregar logging explícito en app/main.py
import logging
logging.basicConfig(level=logging.INFO)

# Reconstruir
docker-compose up --build
```

---

## Recursos Adicionales

- **Documentación API:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`
- **Guía de Arquitectura:** [ARCHITECTURE.md](ARCHITECTURE.md)
- **Guía de API:** [API.md](API.md)
- **Tests:** [tests/README.md](../tests/README.md)
- **Migraciones:** [alembic/README.md](../alembic/README.md)

---

## Contacto y Soporte

Para reportar bugs o solicitar features:
1. Crear issue en repositorio
2. Incluir logs relevantes
3. Describir pasos para reproducir
4. Versión de Python, Docker, y sistema operativo
