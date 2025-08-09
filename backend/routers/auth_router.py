# backend/routers/auth_router.py
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from pydantic import BaseModel
import os

from models import User
from database import get_db
from auth import validate_telegram_data, create_access_token, get_current_user

router = APIRouter(prefix="/api/auth", tags=["authentication"])

class AuthRequest(BaseModel):
    initData: str

class UserResponse(BaseModel):
    id: int
    telegram_id: int
    first_name: str
    last_name: str = None
    username: str = None

class AuthResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

@router.post("/", response_model=AuthResponse)
async def auth_user(auth_request: AuthRequest, db: Session = Depends(get_db)):
    """Аутентификация пользователя через Telegram Web App"""
    
    BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
    
    if BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        # В режиме разработки принимаем любые данные
        # В продакшене нужно установить переменную окружения BOT_TOKEN
        pass
    
    result = validate_telegram_data(auth_request.initData, BOT_TOKEN)
    
    if not result and BOT_TOKEN != "YOUR_BOT_TOKEN_HERE":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired authentication"
        )
    
    # В режиме разработки создаем тестового пользователя
    if not result:
        user_data = {
            "id": 12345,
            "first_name": "Test",
            "last_name": "User",
            "username": "testuser"
        }
    else:
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
    
    return AuthResponse(
        access_token=token,
        token_type="bearer",
        user=UserResponse(
            id=db_user.id,
            telegram_id=db_user.telegram_id,
            first_name=db_user.first_name,
            last_name=db_user.last_name,
            username=db_user.username
        )
    )

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Получение информации о текущем пользователе"""
    return UserResponse(
        id=current_user.id,
        telegram_id=current_user.telegram_id,
        first_name=current_user.first_name,
        last_name=current_user.last_name,
        username=current_user.username
    )
