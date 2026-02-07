"""
Application Configuration.

This module defines the application settings using Pydantic's BaseSettings.
It loads configuration from environment variables and validates them.
"""

from pydantic_settings import BaseSettings
from pydantic import field_validator


class Settings(BaseSettings):
    """
    Application configuration loaded from environment variables.
    
    Attributes:
        database_url (str): The database connection URL.
        jwt_secret (str): Secret key for signing JWT tokens.
        jwt_alg (str): Algorithm used for JWT signing (default: HS256).
        access_token_expire_minutes (int): Token expiration time in minutes.
        timezone (str): Default timezone offset (default: +02:00).
        aws_region (str): AWS region for Bedrock services.
        bedrock_model_id (str): ID of the Bedrock model to use.
    """
    database_url: str
    jwt_secret: str
    jwt_alg: str = "HS256"
    access_token_expire_minutes: int = 60
    timezone: str = "+02:00"  # Default Europe/Madrid (CET)

    aws_region: str = "eu-west-1"
    bedrock_model_id: str = ""
    
    @field_validator('jwt_secret')
    @classmethod
    def validate_jwt_secret(cls, v: str) -> str:
        """
        Ensure JWT secret is strong enough.
        
        Args:
            v (str): The JWT secret value.
            
        Returns:
            str: The validated JWT secret.
            
        Raises:
            ValueError: If the secret is shorter than 32 characters.
        """
        if len(v) < 32:
            raise ValueError('JWT secret must be at least 32 characters for security')
        return v
    
    @field_validator('timezone')
    @classmethod
    def validate_timezone(cls, v: str) -> str:
        """
        Validate timezone format.
        
        Args:
            v (str): The timezone string.
            
        Returns:
            str: The validated timezone string.
            
        Raises:
            ValueError: If the format is incorrect (must be +HH:MM or -HH:MM).
        """
        if not v.startswith(('+', '-')):
            raise ValueError('Timezone must be in format +HH:MM or -HH:MM (e.g., +02:00)')
        return v

    class Config:
        env_file = ".env"


settings = Settings()
