# backend/config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # База данных
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./app.db")
    
    # JWT
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-super-secret-key-change-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "10080"))  # 7 дней
    
    # Telegram Bot
    BOT_TOKEN: str = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
    
    # CORS
    ALLOWED_ORIGINS: list = [
        "http://localhost:3000",
        "http://localhost:5173",
        "https://your-domain.vercel.app",
        "*"  # В продакшене укажите конкретные домены
    ]
    
    # Загрузка файлов
    UPLOAD_DIR: str = "uploads"
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS: list = [".jpg", ".jpeg", ".png", ".gif"]
    
    # API
    API_V1_STR: str = "/api"
    PROJECT_NAME: str = "ЗдравСкан API"
    
    # Подписка
    SUBSCRIPTION_PLANS = {
        "express": {"days": 30, "price": 229},
        "quarter": {"days": 90, "price": 749},
        "annual": {"days": 365, "price": 2499}
    }

settings = Settings()
