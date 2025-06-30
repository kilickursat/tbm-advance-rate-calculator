from pydantic_settings import BaseSettings
from typing import List, Optional
import os

class Settings(BaseSettings):
    APP_NAME: str = "TBM Advance Rate Calculator"
    VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    ALLOWED_HOSTS: List[str] = ["*"]  # Configure properly for production
    
    # Database (for future use)
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./tbm_calculator.db")
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # Model parameters
    MODEL_VERSION: str = "1.0"
    
    # Monitoring (optional fields)
    SENTRY_DSN: Optional[str] = None
    MONITORING_ENABLED: bool = False

    class Config:
        env_file = ".env"
        case_sensitive = True
        # Allow extra fields to prevent validation errors
        extra = "allow"

settings = Settings()
