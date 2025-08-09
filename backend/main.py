# backend/main.py
# Старый main.py - теперь используется app.py
# Этот файл оставлен для совместимости

from app import app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)