# backend/routers/subscription_router.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timedelta

from models import User, Subscription, SubscriptionType, SubscriptionStatus
from database import get_db
from auth import get_current_user

router = APIRouter(prefix="/api/subscription", tags=["subscription"])

class SubscriptionResponse(BaseModel):
    id: int
    subscription_type: str
    status: str
    start_date: datetime
    end_date: datetime
    is_trial: bool
    days_remaining: int
    auto_renew: bool

class CreateSubscriptionRequest(BaseModel):
    subscription_type: str  # "trial", "express", "quarter", "annual"

class SubscriptionStatusResponse(BaseModel):
    has_active_subscription: bool
    subscription: Optional[SubscriptionResponse] = None

def calculate_end_date(subscription_type: SubscriptionType, start_date: datetime) -> datetime:
    """Вычисление даты окончания подписки"""
    if subscription_type == SubscriptionType.TRIAL:
        return start_date + timedelta(days=7)
    elif subscription_type == SubscriptionType.EXPRESS:
        return start_date + timedelta(days=30)
    elif subscription_type == SubscriptionType.QUARTER:
        return start_date + timedelta(days=90)
    elif subscription_type == SubscriptionType.ANNUAL:
        return start_date + timedelta(days=365)
    else:
        raise ValueError("Invalid subscription type")

@router.get("/status", response_model=SubscriptionStatusResponse)
async def get_subscription_status(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Получение статуса подписки пользователя"""
    
    # Ищем активную подписку
    subscription = db.query(Subscription).filter(
        Subscription.user_id == current_user.id,
        Subscription.status == SubscriptionStatus.ACTIVE,
        Subscription.end_date > datetime.utcnow()
    ).order_by(Subscription.end_date.desc()).first()
    
    if not subscription:
        return SubscriptionStatusResponse(has_active_subscription=False)
    
    days_remaining = (subscription.end_date - datetime.utcnow()).days
    
    return SubscriptionStatusResponse(
        has_active_subscription=True,
        subscription=SubscriptionResponse(
            id=subscription.id,
            subscription_type=subscription.subscription_type.value,
            status=subscription.status.value,
            start_date=subscription.start_date,
            end_date=subscription.end_date,
            is_trial=subscription.is_trial,
            days_remaining=max(0, days_remaining),
            auto_renew=subscription.auto_renew
        )
    )

@router.post("/create", response_model=SubscriptionResponse)
async def create_subscription(
    request: CreateSubscriptionRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Создание новой подписки"""
    
    # Проверяем валидность типа подписки
    try:
        subscription_type = SubscriptionType(request.subscription_type)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid subscription type"
        )
    
    # Проверяем, есть ли уже активная подписка
    existing_subscription = db.query(Subscription).filter(
        Subscription.user_id == current_user.id,
        Subscription.status == SubscriptionStatus.ACTIVE,
        Subscription.end_date > datetime.utcnow()
    ).first()
    
    if existing_subscription:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already has an active subscription"
        )
    
    # Проверяем, была ли уже использована пробная подписка
    if subscription_type == SubscriptionType.TRIAL:
        trial_used = db.query(Subscription).filter(
            Subscription.user_id == current_user.id,
            Subscription.is_trial == True
        ).first()
        
        if trial_used:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Trial subscription already used"
            )
    
    # Создаем новую подписку
    start_date = datetime.utcnow()
    end_date = calculate_end_date(subscription_type, start_date)
    
    subscription = Subscription(
        user_id=current_user.id,
        subscription_type=subscription_type,
        status=SubscriptionStatus.ACTIVE,
        start_date=start_date,
        end_date=end_date,
        is_trial=(subscription_type == SubscriptionType.TRIAL),
        auto_renew=(subscription_type != SubscriptionType.TRIAL)
    )
    
    db.add(subscription)
    db.commit()
    db.refresh(subscription)
    
    days_remaining = (subscription.end_date - datetime.utcnow()).days
    
    return SubscriptionResponse(
        id=subscription.id,
        subscription_type=subscription.subscription_type.value,
        status=subscription.status.value,
        start_date=subscription.start_date,
        end_date=subscription.end_date,
        is_trial=subscription.is_trial,
        days_remaining=max(0, days_remaining),
        auto_renew=subscription.auto_renew
    )

@router.post("/{subscription_id}/cancel")
async def cancel_subscription(
    subscription_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Отмена подписки"""
    
    subscription = db.query(Subscription).filter(
        Subscription.id == subscription_id,
        Subscription.user_id == current_user.id
    ).first()
    
    if not subscription:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subscription not found"
        )
    
    subscription.auto_renew = False
    db.commit()
    
    return {"message": "Subscription auto-renewal cancelled"}

@router.get("/plans")
async def get_subscription_plans():
    """Получение доступных планов подписки"""
    
    return {
        "plans": [
            {
                "type": "trial",
                "name": "Пробный период",
                "duration": "7 дней",
                "price": 0,
                "description": "Полный доступ ко всем функциям"
            },
            {
                "type": "express",
                "name": "Экспресс-проверка",
                "duration": "1 месяц",
                "price": 229,
                "description": "Подписка на 1 месяц"
            },
            {
                "type": "quarter",
                "name": "Триместр здоровья",
                "duration": "3 месяца",
                "price": 749,
                "description": "Подписка на 3 месяца"
            },
            {
                "type": "annual",
                "name": "Годовой иммунитет",
                "duration": "12 месяцев",
                "price": 2499,
                "description": "Подписка на 12 месяцев"
            }
        ]
    }
