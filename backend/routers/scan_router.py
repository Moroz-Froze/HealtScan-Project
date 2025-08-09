# backend/routers/scan_router.py
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, BackgroundTasks
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
import json
import os
import uuid
from datetime import datetime
import shutil

from models import User, Scan, QueryHistory, ScanStatus, Subscription, SubscriptionStatus
from database import get_db
from auth import get_current_user
from services.image_analyzer import analyze_medical_image, validate_medical_image

router = APIRouter(prefix="/api/scan", tags=["scanning"])

class ScanResponse(BaseModel):
    id: int
    status: str
    condition_detected: str = None
    description: str = None
    confidence: float = None
    recommendations: List[str] = []
    created_at: datetime
    processed_at: datetime = None

class ScanHistoryResponse(BaseModel):
    scans: List[ScanResponse]
    total: int

# Создание директории для загруженных изображений
UPLOAD_DIR = "uploads/images"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def process_scan_background(scan_id: int, image_path: str):
    """Фоновая обработка сканирования изображения"""
    from database import SessionLocal
    
    # Создаем новую сессию для фоновой задачи
    db = SessionLocal()
    try:
        # Симуляция анализа изображения
        analysis_result = analyze_medical_image(image_path)
        
        # Обновляем результаты в базе данных
        scan = db.query(Scan).filter(Scan.id == scan_id).first()
        if scan:
            scan.status = ScanStatus.COMPLETED
            scan.condition_detected = analysis_result["condition"]
            scan.description = analysis_result["description"]
            scan.confidence = analysis_result["confidence"]
            scan.recommendations = json.dumps(analysis_result["recommendations"], ensure_ascii=False)
            scan.processed_at = datetime.utcnow()
            
            # Добавляем в историю запросов
            query_history = QueryHistory(
                user_id=scan.user_id,
                query_text=analysis_result["condition"],
                scan_id=scan.id
            )
            db.add(query_history)
            
            db.commit()
    except Exception as e:
        # В случае ошибки помечаем скан как неудачный
        scan = db.query(Scan).filter(Scan.id == scan_id).first()
        if scan:
            scan.status = ScanStatus.FAILED
            scan.processed_at = datetime.utcnow()
            db.commit()
    finally:
        db.close()

def check_user_subscription(user: User, db: Session) -> bool:
    """Проверка активной подписки пользователя"""
    subscription = db.query(Subscription).filter(
        Subscription.user_id == user.id,
        Subscription.status == SubscriptionStatus.ACTIVE,
        Subscription.end_date > datetime.utcnow()
    ).first()
    return subscription is not None

@router.post("/upload", response_model=ScanResponse)
async def upload_and_scan_image(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Загрузка изображения и запуск анализа"""
    
    # Проверяем подписку пользователя
    if not check_user_subscription(current_user, db):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Active subscription required to use scan functionality"
        )
    
    # Проверяем тип файла
    if not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must be an image"
        )
    
    # Генерируем уникальное имя файла
    file_extension = file.filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, filename)
    
    # Сохраняем файл
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Проверяем валидность изображения
    if not validate_medical_image(file_path):
        os.remove(file_path)  # Удаляем невалидный файл
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid image format or resolution. Please upload a valid medical image."
        )
    
    # Создаем запись в базе данных
    scan = Scan(
        user_id=current_user.id,
        image_path=file_path,
        status=ScanStatus.PROCESSING
    )
    db.add(scan)
    db.commit()
    db.refresh(scan)
    
    # Запускаем фоновую обработку
    background_tasks.add_task(process_scan_background, scan.id, file_path)
    
    return ScanResponse(
        id=scan.id,
        status=scan.status.value,
        created_at=scan.created_at
    )

@router.get("/{scan_id}", response_model=ScanResponse)
async def get_scan_result(
    scan_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Получение результата сканирования"""
    
    scan = db.query(Scan).filter(
        Scan.id == scan_id,
        Scan.user_id == current_user.id
    ).first()
    
    if not scan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scan not found"
        )
    
    recommendations = []
    if scan.recommendations:
        try:
            recommendations = json.loads(scan.recommendations)
        except json.JSONDecodeError:
            recommendations = []
    
    return ScanResponse(
        id=scan.id,
        status=scan.status.value,
        condition_detected=scan.condition_detected,
        description=scan.description,
        confidence=scan.confidence,
        recommendations=recommendations,
        created_at=scan.created_at,
        processed_at=scan.processed_at
    )

@router.get("/", response_model=ScanHistoryResponse)
async def get_scan_history(
    limit: int = 10,
    offset: int = 0,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Получение истории сканирований пользователя"""
    
    total = db.query(Scan).filter(Scan.user_id == current_user.id).count()
    
    scans = db.query(Scan).filter(
        Scan.user_id == current_user.id
    ).order_by(Scan.created_at.desc()).offset(offset).limit(limit).all()
    
    scan_responses = []
    for scan in scans:
        recommendations = []
        if scan.recommendations:
            try:
                recommendations = json.loads(scan.recommendations)
            except json.JSONDecodeError:
                recommendations = []
        
        scan_responses.append(ScanResponse(
            id=scan.id,
            status=scan.status.value,
            condition_detected=scan.condition_detected,
            description=scan.description,
            confidence=scan.confidence,
            recommendations=recommendations,
            created_at=scan.created_at,
            processed_at=scan.processed_at
        ))
    
    return ScanHistoryResponse(
        scans=scan_responses,
        total=total
    )
