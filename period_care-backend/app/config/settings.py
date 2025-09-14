from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Database Options
    database_type: str = "sqlite"  # "firebase" or "postgresql" or "sqlite"
    database_url: str = "sqlite:///./periodcare.db"  # Fallback for SQL databases
    
    # Firebase Configuration
    firebase_service_account_path: str = "./firebase-service-account.json"
    firebase_project_id: Optional[str] = None
    use_firebase: bool = False  # Toggle Firebase usage
    
    # Security
    secret_key: str = "your-secret-key-here-change-this-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    
    # WhatsApp
    admin_whatsapp_number: str = "+917339625044"
    
    # Frontend
    frontend_url: str = "http://localhost:5173"
    
    # Reminders
    reminder_check_time: str = "09:00"
    
    # Email
    smtp_server: str = "smtp.gmail.com"
    smtp_username: Optional[str] = None
    smtp_password: Optional[str] = None
    
    # Redis
    redis_url: str = "redis://localhost:6379"
    
    # Development
    debug: bool = True
    environment: str = "development"
    
    class Config:
        env_file = ".env"


settings = Settings()
