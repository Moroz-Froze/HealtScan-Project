#!/usr/bin/env python3
"""
Скрипт для запуска бэкенда ЗдравСкан
"""

import uvicorn
import os
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

if __name__ == "__main__":
    # Настройки сервера
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    reload = os.getenv("DEBUG", "False").lower() == "true"
    
    print(f"🚀 Запуск ЗдравСкан Backend на {host}:{port}")
    print(f"📖 Документация: http://{host}:{port}/docs")
    print(f"🔍 ReDoc: http://{host}:{port}/redoc")
    
    # Запуск сервера
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=reload,
        log_level="info"
    )
