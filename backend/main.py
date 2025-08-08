# backend/main.py
from fastapi import FastAPI, Depends, HTTPException, Request, status, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from jose import jwt, JWTError
import json
import hashlib
import hmac
from urllib.parse import parse_qsl
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
import os
import base64
from io import BytesIO
from PIL import Image
import requests

# --- Подключение к базе данных ---
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Настройка БД
SQLALCHEMY_DATABASE_URL = "sqlite:///./app.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Модели базы данных
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(Integer, unique=True, index=True)
    first_name = Column(String(100))
    last_name = Column(String(100), nullable=True)
    username = Column(String(100), nullable=True)
    subscription_expires = Column(DateTime, nullable=True)
    is_subscribed = Column(Boolean, default=False)

class ScanHistory(Base):
    __tablename__ = "scan_history"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    image_path = Column(String(500))
    result = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

class Literature(Base):
    __tablename__ = "literature"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200))
    description = Column(Text)
    file_path = Column(String(500), nullable=True)
    category = Column(String(100))

Base.metadata.create_all(bind=engine)

# --- FastAPI приложение ---
app = FastAPI(
    title="ЗдравСкан API",
    description="API для медицинского приложения ЗдравСкан",
    version="1.0.0"
)

# --- CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В продакшене укажите конкретные домены
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
SECRET_KEY = "your-super-secret-key-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 дней

def create_access_token(data: Dict[str, Any]) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str) -> Optional[Dict[str, Any]]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

# --- Валидация initData от Telegram ---
def validate_telegram_data(init_data: str, bot_token: str) -> Optional[Dict[str, Any]]:
    try:
        params = dict(parse_qsl(init_data))
    except Exception:
        return None

    hash_val = params.pop('hash', None)
    if not hash_val:
        return None

    sorted_params = sorted(params.items())
    data_check_string = '\n'.join([f"{k}={v}" for k, v in sorted_params])

    secret_key = hmac.new(b"WebAppBotToken", bot_token.encode(), hashlib.sha256).digest()
    calculated_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()

    if calculated_hash != hash_val:
        return None

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

# --- Зависимость для аутентификации ---
async def get_current_user(request: Request, db: Session = Depends(get_db)):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )
    
    token = auth_header.split(" ")[1]
    payload = verify_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    
    user_id = payload.get("user_id")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    return user

# --- Роуты ---

@app.post("/api/auth")
async def auth_user(request: Request, db: Session = Depends(get_db)):
    """Аутентификация пользователя через Telegram"""
    try:
        form_data = await request.json()
        init_data = form_data.get("initData")

        if not init_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="initData is required"
            )

        BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"  # Замените на свой токен
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
                "username": db_user.username,
                "is_subscribed": db_user.is_subscribed,
                "subscription_expires": db_user.subscription_expires.isoformat() if db_user.subscription_expires else None
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@app.post("/api/scan")
async def scan_image(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Сканирование изображения для медицинской диагностики"""
    try:
        # Проверяем подписку
        if not current_user.is_subscribed:
            raise HTTPException(
                status_code=status.HTTP_402_PAYMENT_REQUIRED,
                detail="Subscription required"
            )

        # Сохраняем изображение
        image_data = await file.read()
        image = Image.open(BytesIO(image_data))
        
        # Создаем папку для изображений если её нет
        os.makedirs("uploads", exist_ok=True)
        
        # Сохраняем изображение
        filename = f"scan_{current_user.id}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.jpg"
        file_path = f"uploads/{filename}"
        image.save(file_path, "JPEG")

        # Здесь должна быть логика анализа изображения
        # Пока возвращаем демо-результат
        result = {
            "condition": "Укус слепня",
            "description": "В большинстве случаев укус слепня для человека неприятен, но не опасен. Однако при склонности к аллергии или множественных укусах нужно обязательно обратиться к врачу.",
            "recommendations": [
                "Промойте место укуса холодной водой",
                "Приложите лед для уменьшения отека",
                "Используйте антигистаминные препараты при аллергии",
                "Обратитесь к врачу при сильной реакции"
            ],
            "confidence": 0.85
        }

        # Сохраняем в историю
        scan_record = ScanHistory(
            user_id=current_user.id,
            image_path=file_path,
            result=json.dumps(result)
        )
        db.add(scan_record)
        db.commit()

        return {
            "success": True,
            "result": result,
            "image_path": file_path
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@app.get("/api/history")
async def get_scan_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Получение истории сканирований пользователя"""
    try:
        history = db.query(ScanHistory).filter(
            ScanHistory.user_id == current_user.id
        ).order_by(ScanHistory.created_at.desc()).limit(10).all()

        return {
            "history": [
                {
                    "id": item.id,
                    "result": json.loads(item.result),
                    "created_at": item.created_at.isoformat(),
                    "image_path": item.image_path
                }
                for item in history
            ]
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@app.get("/api/literature")
async def get_literature(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Получение списка справочной литературы"""
    try:
        literature = db.query(Literature).all()
        
        return {
            "literature": [
                {
                    "id": item.id,
                    "title": item.title,
                    "description": item.description,
                    "category": item.category,
                    "file_path": item.file_path
                }
                for item in literature
            ]
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@app.post("/api/subscription")
async def create_subscription(
    subscription_data: Dict[str, Any],
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Создание подписки пользователя"""
    try:
        plan = subscription_data.get("plan")
        duration_days = {
            "express": 30,
            "quarter": 90,
            "annual": 365
        }.get(plan, 30)

        current_user.is_subscribed = True
        current_user.subscription_expires = datetime.utcnow() + timedelta(days=duration_days)
        
        db.commit()

        return {
            "success": True,
            "subscription_expires": current_user.subscription_expires.isoformat(),
            "is_subscribed": current_user.is_subscribed
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@app.get("/api/user/profile")
async def get_user_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Получение профиля пользователя"""
    try:
        return {
            "user": {
                "id": current_user.id,
                "telegram_id": current_user.telegram_id,
                "first_name": current_user.first_name,
                "last_name": current_user.last_name,
                "username": current_user.username,
                "is_subscribed": current_user.is_subscribed,
                "subscription_expires": current_user.subscription_expires.isoformat() if current_user.subscription_expires else None
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@app.get("/")
def read_root():
    return {
        "message": "ЗдравСкан API работает!",
        "version": "1.0.0",
        "endpoints": {
            "auth": "/api/auth",
            "scan": "/api/scan",
            "history": "/api/history",
            "literature": "/api/literature",
            "subscription": "/api/subscription",
            "profile": "/api/user/profile"
        }
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)