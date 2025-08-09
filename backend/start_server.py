#!/usr/bin/env python3
# backend/start_server.py

import os
import uvicorn
from app import app

# Настройка переменных окружения для продакшена
os.environ.setdefault("SECRET_KEY", "healthscan-super-secret-key-2024-production")
os.environ.setdefault("BOT_TOKEN", "YOUR_TELEGRAM_BOT_TOKEN_HERE")
os.environ.setdefault("DATABASE_URL", "sqlite:///./app.db")

def main():
    print("🚀 Запуск HealthScan Backend Server...")
    print(f"📍 Фронтенд: https://moroz-froze-healtscan-project-cce0.twc1.net")
    print(f"🌐 Backend API: http://localhost:8000")
    print(f"📚 Документация: http://localhost:8000/docs")
    print("=" * 50)
    
    # Запуск сервера
    uvicorn.run(
        "app:app",
        host="127.0.0.1",
        port=8000,
        reload=True,  # Автоперезагрузка при изменениях
        log_level="info"
    )

if __name__ == "__main__":
    main()
