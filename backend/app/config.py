"""Application configuration."""

import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    """Application settings."""
    
    # Database
    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "postgresql://attendance_user:secure_password_here@localhost:5432/attendance_db"
    )
    
    # FastAPI
    APP_NAME = "Web Attendance Tracker API"
    APP_VERSION = "1.0.0"
    DEBUG = os.getenv("FASTAPI_DEBUG", "True").lower() == "true"
    
    # CORS
    ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:8000").split(",")
    
    # AI/ML
    ML_ENABLED = os.getenv("ML_ENABLED", "True").lower() == "true"
    ANOMALY_THRESHOLD = float(os.getenv("ANOMALY_THRESHOLD", "0.7"))

settings = Settings()
