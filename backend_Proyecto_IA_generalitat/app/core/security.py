from datetime import datetime, timedelta, timezone
import hashlib

from jose import jwt
from passlib.context import CryptContext

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def _bcrypt_input(password: str) -> str:
    """
    Pre-hash password with SHA-256 to support long passwords (bcrypt has 72-byte limit).
    """
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    return pwd_context.hash(_bcrypt_input(password))


def verify_password(password: str, password_hash: str) -> bool:
    """Verify a password against its hash."""
    return pwd_context.verify(_bcrypt_input(password), password_hash)


def create_access_token(subject: str) -> str:
    """Create a JWT access token for the given subject (user ID)."""
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.access_token_expire_minutes
    )
    payload = {"sub": subject, "exp": expire}
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_alg)


def decode_token(token: str) -> dict:
    """Decode and validate a JWT token."""
    return jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_alg])
