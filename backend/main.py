# backend/main.py
from fastapi import FastAPI, Depends, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from jose import jwt
import json
import hashlib
import hmac
from urllib.parse import parse_qsl
from datetime import datetime, timedelta
from typing import Dict, Any

# --- Подключение к базе данных ---
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Настройка БД (можно вынести в отдельный файл)
SQLALCHEMY_DATABASE_URL = "sqlite:///./app.db"  # Или PostgreSQL: "postgresql://user:pass@localhost/db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(Integer, unique=True, index=True)
    first_name = Column(String(100))
    last_name = Column(String(100), nullable=True)
    username = Column(String(100), nullable=True)

Base.metadata.create_all(bind=engine)

# --- FastAPI приложение ---
app = FastAPI(title="Telegram Mini App API")

# --- CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-mini-app.com", "https://your-domain.vercel.app"],  # Замени на свой домен
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Зависимость для БД ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- JWT конфигурация ---
SECRET_KEY = "your-super-secret-key-change-in-production"  # Обязательно замени!
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 дней

def create_access_token(data: Dict[str, Any]) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# --- Валидация initData от Telegram ---
def validate_telegram_data(init_data: str, bot_token: str) -> Dict[str, Any]:
    """
    Проверяет подпись initData от Telegram Web App.
    Возвращает данные пользователя или None.
    """
    try:
        params = dict(parse_qsl(init_data))
    except Exception:
        return None

    hash_val = params.pop('hash', None)
    if not hash_val:
        return None

    # Сортируем параметры по ключу
    sorted_params = sorted(params.items())
    data_check_string = '\n'.join([f"{k}={v}" for k, v in sorted_params])

    # Создаём secret_key = HMAC-SHA256("WebAppBotToken", bot_token)
    secret_key = hmac.new(b"WebAppBotToken", bot_token.encode(), hashlib.sha256).digest()

    # Вычисляем хэш
    calculated_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()

    if calculated_hash != hash_val:
        return None

    # Парсим данные пользователя
    user_str = params.get("user")
    if not user_str:
        return None

    try:
        user_data = json.loads(user_str)
        return {
            "user": user_data,
            "auth_date": params.get("auth_date"),
            "hash": hash_val
        }
    except json.JSONDecodeError:
        return None

# --- Роут аутентификации ---
@app.post("/api/auth")
async def auth_user(request: Request, db: Session = Depends(get_db)):
    form_data = await request.json()
    init_data = form_data.get("initData")

    if not init_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="initData is required"
        )

    BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"  # ← ЗАМЕНИ НА СВОЙ ТОКЕН!
    result = validate_telegram_data(init_data, BOT_TOKEN)

    if not result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired authentication"
        )

    user_data = result["user"]
    telegram_id = user_data["id"]

    # Проверяем, есть ли пользователь
    db_user = db.query(User).filter(User.telegram_id == telegram_id).first()
    if not db_user:
        db_user = User(
            telegram_id=telegram_id,
            first_name=user_data.get("first_name"),
            last_name=user_data.get("last_name"),
            username=user_data.get("username")
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

    # Генерируем JWT
    token = create_access_token({"user_id": db_user.id, "telegram_id": telegram_id})

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": db_user.id,
            "telegram_id": db_user.telegram_id,
            "first_name": db_user.first_name,
            "last_name": db_user.last_name,
            "username": db_user.username
        }
    }

# --- Корневой маршрут ---
@app.get("/")
def read_root():
    return {"message": "Telegram Mini App Backend is running! Use /api/auth to login."}