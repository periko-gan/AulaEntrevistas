"""
Security Utilities.

This module provides functions for password hashing, verification, and JWT token management.
It handles the security aspects of user authentication.
"""

from datetime import datetime, timedelta, timezone
import hashlib

from jose import jwt
from passlib.context import CryptContext

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def _bcrypt_input(password: str) -> str:
    """
    Pre-hash password with SHA-256 to support long passwords (bcrypt has 72-byte limit).
    
    Args:
        password (str): The plain text password.
        
    Returns:
        str: The SHA-256 hash of the password.
    """
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt.
    
    Args:
        password (str): The plain text password.
        
    Returns:
        str: The hashed password.
    """
    return pwd_context.hash(_bcrypt_input(password))


def verify_password(password: str, password_hash: str) -> bool:
    """
    Verify a password against its hash.
    
    Args:
        password (str): The plain text password to verify.
        password_hash (str): The stored password hash.
        
    Returns:
        bool: True if the password matches the hash, False otherwise.
    """
    return pwd_context.verify(_bcrypt_input(password), password_hash)


def create_access_token(subject: str) -> str:
    """
    Create a JWT access token for the given subject (user ID).
    
    Args:
        subject (str): The subject identifier (usually user ID).
        
    Returns:
        str: The encoded JWT access token.
    """
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.access_token_expire_minutes
    )
    payload = {"sub": subject, "exp": expire}
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_alg)


def decode_token(token: str) -> dict:
    """
    Decode and validate a JWT token.
    
    Args:
        token (str): The JWT token to decode.
        
    Returns:
        dict: The decoded token payload.
        
    Raises:
        JWTError: If the token is invalid or expired.
    """
    return jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_alg])
