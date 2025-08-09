# backend/auth.py
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
import json
import hashlib
import hmac
from urllib.parse import parse_qsl
import os

from models import User
from database import get_db

# JWT конфигурация
SECRET_KEY = os.getenv("SECRET_KEY", "your-super-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 дней

security = HTTPBearer()

def create_access_token(data: Dict[str, Any]) -> str:
    """Создание JWT токена"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str) -> Optional[Dict[str, Any]]:
    """Проверка JWT токена"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

def validate_telegram_data(init_data: str, bot_token: str) -> Optional[Dict[str, Any]]:
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

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """Получение текущего пользователя из JWT токена"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    token = credentials.credentials
    payload = verify_token(token)
    
    if payload is None:
        raise credentials_exception
    
    user_id: int = payload.get("user_id")
    if user_id is None:
        raise credentials_exception
    
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise credentials_exception
    
    return user

security_optional = HTTPBearer(auto_error=False)

def get_current_user_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security_optional),
    db: Session = Depends(get_db)
) -> Optional[User]:
    """Получение текущего пользователя (опционально)"""
    if credentials is None:
        return None
    
    try:
        token = credentials.credentials
        payload = verify_token(token)
        
        if payload is None:
            return None
        
        user_id: int = payload.get("user_id")
        if user_id is None:
            return None
        
        user = db.query(User).filter(User.id == user_id).first()
        return user
    except Exception:
        return None