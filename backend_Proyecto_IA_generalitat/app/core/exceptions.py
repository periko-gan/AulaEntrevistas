"""Global exception handlers for FastAPI application."""
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError
from jose import JWTError
import logging

logger = logging.getLogger(__name__)


async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle all unhandled exceptions."""
    logger.error(
        f"Unhandled exception in {request.method} {request.url.path}",
        exc_info=True,
        extra={
            "method": request.method,
            "path": request.url.path,
            "error_type": type(exc).__name__
        }
    )
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "Internal server error. Please try again later.",
            "error_type": type(exc).__name__
        }
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """Handle Pydantic validation errors with detailed messages."""
    errors = []
    for error in exc.errors():
        field = " -> ".join(str(x) for x in error["loc"])
        errors.append({
            "field": field,
            "message": error["msg"],
            "type": error["type"]
        })
    
    logger.warning(
        f"Validation error in {request.method} {request.url.path}",
        extra={"errors": errors}
    )
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": "Validation error",
            "errors": errors
        }
    )


async def database_exception_handler(request: Request, exc: SQLAlchemyError) -> JSONResponse:
    """Handle database-related errors."""
    logger.error(
        f"Database error in {request.method} {request.url.path}",
        exc_info=True,
        extra={
            "error_type": type(exc).__name__
        }
    )
    
    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content={
            "detail": "Database service temporarily unavailable. Please try again later.",
            "error_type": "DatabaseError"
        }
    )


async def jwt_exception_handler(request: Request, exc: JWTError) -> JSONResponse:
    """Handle JWT token errors."""
    logger.warning(
        f"JWT error in {request.method} {request.url.path}",
        extra={
            "error_type": type(exc).__name__,
            "token_present": "Authorization" in request.headers
        }
    )
    
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={
            "detail": "Invalid or expired authentication token",
            "error_type": "AuthenticationError"
        },
        headers={"WWW-Authenticate": "Bearer"}
    )
