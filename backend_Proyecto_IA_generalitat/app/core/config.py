from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""
    database_url: str
    jwt_secret: str
    jwt_alg: str = "HS256"
    access_token_expire_minutes: int = 60

    aws_region: str = "eu-west-1"
    bedrock_model_id: str = ""

    class Config:
        env_file = ".env"

settings = Settings()
