from pydantic_settings import BaseSettings
from pydantic import field_validator


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""
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
        """Ensure JWT secret is strong enough."""
        if len(v) < 32:
            raise ValueError('JWT secret must be at least 32 characters for security')
        return v
    
    @field_validator('timezone')
    @classmethod
    def validate_timezone(cls, v: str) -> str:
        """Validate timezone format."""
        if not v.startswith(('+', '-')):
            raise ValueError('Timezone must be in format +HH:MM or -HH:MM (e.g., +02:00)')
        return v

    class Config:
        env_file = ".env"


settings = Settings()
