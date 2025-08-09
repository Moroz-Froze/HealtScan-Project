# backend/routers/history_router.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
from datetime import datetime

from models import User, QueryHistory
from database import get_db
from auth import get_current_user

router = APIRouter(prefix="/api/history", tags=["history"])

class QueryHistoryResponse(BaseModel):
    id: int
    query_text: str
    scan_id: int = None
    created_at: datetime

class HistoryListResponse(BaseModel):
    history: List[QueryHistoryResponse]
    total: int

@router.get("/", response_model=HistoryListResponse)
async def get_query_history(
    limit: int = 20,
    offset: int = 0,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Получение истории запросов пользователя"""
    
    total = db.query(QueryHistory).filter(
        QueryHistory.user_id == current_user.id
    ).count()
    
    history_items = db.query(QueryHistory).filter(
        QueryHistory.user_id == current_user.id
    ).order_by(QueryHistory.created_at.desc()).offset(offset).limit(limit).all()
    
    history_responses = []
    for item in history_items:
        history_responses.append(QueryHistoryResponse(
            id=item.id,
            query_text=item.query_text,
            scan_id=item.scan_id,
            created_at=item.created_at
        ))
    
    return HistoryListResponse(
        history=history_responses,
        total=total
    )

@router.delete("/{history_id}")
async def delete_history_item(
    history_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Удаление элемента из истории"""
    
    history_item = db.query(QueryHistory).filter(
        QueryHistory.id == history_id,
        QueryHistory.user_id == current_user.id
    ).first()
    
    if history_item:
        db.delete(history_item)
        db.commit()
        return {"message": "History item deleted"}
    else:
        return {"message": "History item not found"}

@router.delete("/")
async def clear_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Очистка всей истории пользователя"""
    
    db.query(QueryHistory).filter(
        QueryHistory.user_id == current_user.id
    ).delete()
    db.commit()
    
    return {"message": "History cleared"}
