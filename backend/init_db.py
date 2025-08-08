# backend/init_db.py
from main import SessionLocal, Literature
from datetime import datetime

def init_database():
    db = SessionLocal()
    
    # Добавляем демо-литературу
    literature_items = [
        {
            "title": "Справочник по клинической офтальмологии",
            "description": "Подробное руководство по диагностике и лечению заболеваний глаз",
            "category": "Офтальмология",
            "file_path": "/literature/ophthalmology_guide.pdf"
        },
        {
            "title": "Инсектная аллергия: диагностика и лечение",
            "description": "Современные методы диагностики и лечения аллергических реакций на укусы насекомых",
            "category": "Аллергология",
            "file_path": "/literature/insect_allergy.pdf"
        },
        {
            "title": "Практическое руководство по неотложной помощи при укусах насекомых",
            "description": "Алгоритмы оказания первой помощи при различных укусах насекомых",
            "category": "Неотложная помощь",
            "file_path": "/literature/emergency_insect_bites.pdf"
        },
        {
            "title": "Кариес зубов: современные методы диагностики",
            "description": "Современные подходы к диагностике и лечению кариеса зубов",
            "category": "Стоматология",
            "file_path": "/literature/dental_caries.pdf"
        },
        {
            "title": "Аллергология и иммунология",
            "description": "Основы аллергологии и иммунологии для практикующих врачей",
            "category": "Аллергология",
            "file_path": "/literature/allergology_immunology.pdf"
        }
    ]
    
    # Проверяем, есть ли уже данные
    existing = db.query(Literature).count()
    if existing == 0:
        for item in literature_items:
            literature = Literature(**item)
            db.add(literature)
        
        db.commit()
        print("✅ База данных инициализирована с демо-данными")
    else:
        print("ℹ️ База данных уже содержит данные")

if __name__ == "__main__":
    init_database()
