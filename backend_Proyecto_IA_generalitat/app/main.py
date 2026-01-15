from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from jose import JWTError
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from datetime import datetime
import logging

from app.core.database import Base, engine
from app.api.v1.router import router as v1_router
from app.core.exceptions import (
    global_exception_handler,
    validation_exception_handler,
    database_exception_handler,
    jwt_exception_handler
)

# Register models with SQLAlchemy
from app.models.user import User  # noqa: F401
from app.models.chat import Chat  # noqa: F401
from app.models.message import Message  # noqa: F401


# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address, default_limits=["100/minute"])

app = FastAPI(title="Aula Virtual - IA Entrevistador", version="1.0.0")
app.state.limiter = limiter

# Register exception handlers
app.add_exception_handler(Exception, global_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(SQLAlchemyError, database_exception_handler)
app.add_exception_handler(JWTError, jwt_exception_handler)
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

logger = logging.getLogger(__name__)

app.include_router(v1_router, prefix="/api/v1")


@app.get("/health")
async def health_check(request: Request):
    """Comprehensive health check endpoint."""
    from app.core.database import get_db
    from app.core.config import settings
    import boto3
    
    checks = {
        "api": "ok",
        "timestamp": datetime.now().isoformat()
    }
    
    # Check database connection
    try:
        db = next(get_db())
        db.execute("SELECT 1")
        checks["database"] = "ok"
    except Exception as e:
        checks["database"] = "error"
        checks["database_error"] = str(e)
        logger.error(f"Database health check failed: {e}")
    
    # Check AWS Bedrock (optional, don't fail if credentials are temporary)
    try:
        client = boto3.client('bedrock-runtime', region_name=settings.aws_region)
        # Just check client creation, don't make actual call
        checks["aws"] = "ok"
    except Exception as e:
        checks["aws"] = "degraded"
        checks["aws_note"] = "AWS client initialization failed (may be temporary credentials)"
        logger.warning(f"AWS health check degraded: {e}")
    
    # Determine overall status
    all_ok = all(
        v == "ok" or k.endswith("_note") or k == "timestamp" or k == "aws" and v == "degraded"
        for k, v in checks.items()
    )
    
    status_code = 200 if all_ok else 503
    
    return JSONResponse(content=checks, status_code=status_code)


@app.get("/")
def root():
    """API root endpoint."""
    return {
        "name": "Aula Virtual - IA Entrevistador API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs",
        "health": "/health"
    }
