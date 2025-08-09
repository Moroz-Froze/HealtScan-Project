# backend/routers/literature_router.py
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
import json

from models import Literature, QueryHistory
from database import get_db
from auth import get_current_user, get_current_user_optional

router = APIRouter(prefix="/api/literature", tags=["literature"])

class LiteratureResponse(BaseModel):
    id: int
    title: str
    description: str = None
    category: str
    author: str = None
    tags: List[str] = []

class LiteratureDetailResponse(BaseModel):
    id: int
    title: str
    description: str = None
    content: str
    category: str
    author: str = None
    tags: List[str] = []

class LiteratureListResponse(BaseModel):
    literature: List[LiteratureResponse]
    total: int
    categories: List[str]

def parse_tags(tags_json: str) -> List[str]:
    """Парсинг тегов из JSON"""
    if not tags_json:
        return []
    try:
        return json.loads(tags_json)
    except json.JSONDecodeError:
        return []

@router.get("/", response_model=LiteratureListResponse)
async def get_literature_list(
    category: Optional[str] = Query(None, description="Фильтр по категории"),
    search: Optional[str] = Query(None, description="Поиск по названию или описанию"),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    """Получение списка справочной литературы"""
    
    query = db.query(Literature).filter(Literature.is_active == True)
    
    # Фильтрация по категории
    if category:
        query = query.filter(Literature.category == category)
    
    # Поиск по тексту
    if search:
        search_filter = f"%{search}%"
        query = query.filter(
            (Literature.title.ilike(search_filter)) |
            (Literature.description.ilike(search_filter))
        )
    
    total = query.count()
    
    literature_items = query.order_by(Literature.title).offset(offset).limit(limit).all()
    
    # Получаем список всех доступных категорий
    categories = db.query(Literature.category).filter(
        Literature.is_active == True
    ).distinct().all()
    categories_list = [cat[0] for cat in categories]
    
    literature_responses = []
    for item in literature_items:
        literature_responses.append(LiteratureResponse(
            id=item.id,
            title=item.title,
            description=item.description,
            category=item.category,
            author=item.author,
            tags=parse_tags(item.tags)
        ))
    
    return LiteratureListResponse(
        literature=literature_responses,
        total=total,
        categories=categories_list
    )

@router.get("/{literature_id}", response_model=LiteratureDetailResponse)
async def get_literature_detail(
    literature_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user_optional)
):
    """Получение подробной информации о справочной литературе"""
    
    literature = db.query(Literature).filter(
        Literature.id == literature_id,
        Literature.is_active == True
    ).first()
    
    if not literature:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Literature not found"
        )
    
    # Если пользователь авторизован, добавляем в историю
    if current_user:
        query_history = QueryHistory(
            user_id=current_user.id,
            query_text=f"Литература: {literature.title}",
            scan_id=None
        )
        db.add(query_history)
        db.commit()
    
    return LiteratureDetailResponse(
        id=literature.id,
        title=literature.title,
        description=literature.description,
        content=literature.content,
        category=literature.category,
        author=literature.author,
        tags=parse_tags(literature.tags)
    )

@router.get("/categories/")
async def get_categories(db: Session = Depends(get_db)):
    """Получение списка категорий литературы"""
    
    categories = db.query(Literature.category).filter(
        Literature.is_active == True
    ).distinct().all()
    
    return {
        "categories": [cat[0] for cat in categories]
    }

@router.get("/search/")
async def search_literature(
    q: str = Query(..., min_length=2, description="Поисковый запрос"),
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """Поиск в справочной литературе"""
    
    search_filter = f"%{q}%"
    
    literature_items = db.query(Literature).filter(
        Literature.is_active == True,
        (Literature.title.ilike(search_filter)) |
        (Literature.description.ilike(search_filter)) |
        (Literature.content.ilike(search_filter))
    ).limit(limit).all()
    
    results = []
    for item in literature_items:
        results.append({
            "id": item.id,
            "title": item.title,
            "description": item.description,
            "category": item.category,
            "relevance_snippet": item.description[:200] + "..." if item.description and len(item.description) > 200 else item.description
        })
    
    return {
        "results": results,
        "total": len(results),
        "query": q
    }
