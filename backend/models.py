# backend/models.py
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Float, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base
import enum

class SubscriptionType(enum.Enum):
    TRIAL = "trial"
    EXPRESS = "express"  # 1 месяц
    QUARTER = "quarter"  # 3 месяца
    ANNUAL = "annual"    # 12 месяцев

class SubscriptionStatus(enum.Enum):
    ACTIVE = "active"
    EXPIRED = "expired"
    CANCELLED = "cancelled"

class ScanStatus(enum.Enum):
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(Integer, unique=True, index=True)
    first_name = Column(String(100))
    last_name = Column(String(100), nullable=True)
    username = Column(String(100), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Связи
    subscriptions = relationship("Subscription", back_populates="user")
    scans = relationship("Scan", back_populates="user")

class Subscription(Base):
    __tablename__ = "subscriptions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    subscription_type = Column(Enum(SubscriptionType))
    status = Column(Enum(SubscriptionStatus), default=SubscriptionStatus.ACTIVE)
    start_date = Column(DateTime(timezone=True), server_default=func.now())
    end_date = Column(DateTime(timezone=True))
    is_trial = Column(Boolean, default=False)
    auto_renew = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Связи
    user = relationship("User", back_populates="subscriptions")

class Scan(Base):
    __tablename__ = "scans"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    image_path = Column(String(500))  # Путь к загруженному изображению
    status = Column(Enum(ScanStatus), default=ScanStatus.PROCESSING)
    condition_detected = Column(String(200), nullable=True)  # Обнаруженное состояние
    description = Column(Text, nullable=True)  # Описание
    confidence = Column(Float, nullable=True)  # Уверенность в диагнозе (0-1)
    recommendations = Column(Text, nullable=True)  # JSON с рекомендациями
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    processed_at = Column(DateTime(timezone=True), nullable=True)
    
    # Связи
    user = relationship("User", back_populates="scans")

class Literature(Base):
    __tablename__ = "literature"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(300))
    description = Column(Text, nullable=True)
    content = Column(Text)  # Текст статьи или ссылка на файл
    category = Column(String(100))  # Категория (офтальмология, аллергология и т.д.)
    tags = Column(Text, nullable=True)  # JSON с тегами
    author = Column(String(200), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    is_active = Column(Boolean, default=True)

class QueryHistory(Base):
    __tablename__ = "query_history"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    query_text = Column(String(500))  # Текст запроса или обнаруженное состояние
    scan_id = Column(Integer, ForeignKey("scans.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Связи
    user = relationship("User")
    scan = relationship("Scan")
