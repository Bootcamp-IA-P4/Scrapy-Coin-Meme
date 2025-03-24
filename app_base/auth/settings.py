import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    
    # JWT settings
    JWT_SECRET_KEY: str = os.environ.get("JWT_SECRET_KEY", "supersecretkey")
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

settings = Settings()