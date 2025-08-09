# backend/app.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from database import engine, Base
from routers import auth_router, scan_router, subscription_router, literature_router, history_router

# Создание таблиц в базе данных
Base.metadata.create_all(bind=engine)

# Создание приложения FastAPI
app = FastAPI(
    title="HealthScan API",
    description="API для приложения медицинского сканирования ЗдравСкан",
    version="1.0.0"
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "https://moroz-froze-healtscan-project-cce0.twc1.net",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        "*"  # Разрешить все домены для тестирования
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение роутеров
app.include_router(auth_router.router)
app.include_router(scan_router.router)
app.include_router(subscription_router.router)
app.include_router(literature_router.router)
app.include_router(history_router.router)

# Статические файлы для загруженных изображений
upload_dir = "uploads"
if not os.path.exists(upload_dir):
    os.makedirs(upload_dir)

app.mount("/uploads", StaticFiles(directory=upload_dir), name="uploads")

# Корневой маршрут
@app.get("/")
def read_root():
    return {
        "message": "HealthScan Backend API",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "running"
    }

# Проверка здоровья приложения
@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "healthscan-backend"
    }

# Обработка ошибок
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return {"error": "Not found", "message": "The requested resource was not found"}

@app.exception_handler(500)
async def internal_error_handler(request, exc):
    return {"error": "Internal server error", "message": "Something went wrong"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

