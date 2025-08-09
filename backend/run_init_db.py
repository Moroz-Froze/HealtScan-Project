# backend/run_init_db.py
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base, Literature
import json

def init_database():
    """Инициализация базы данных с тестовыми данными"""
    
    # Создание всех таблиц
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # Проверяем, есть ли уже данные в таблице литературы
        existing_literature = db.query(Literature).first()
        if existing_literature:
            print("База данных уже содержит данные")
            return
        
        # Добавляем тестовую справочную литературу
        literature_data = [
            {
                "title": "Справочник по клинической офтальмологии",
                "description": "Полное руководство по диагностике и лечению заболеваний глаз",
                "content": "Подробное описание офтальмологических заболеваний...",
                "category": "Офтальмология",
                "author": "Д.м.н. Иванов И.И.",
                "tags": json.dumps(["глаза", "зрение", "конъюнктивит", "ячмень"], ensure_ascii=False)
            },
            {
                "title": "Инсектная аллергия: диагностика и лечение",
                "description": "Руководство по диагностике и лечению аллергических реакций на укусы насекомых",
                "content": "Подробное описание аллергических реакций...",
                "category": "Аллергология",
                "author": "К.м.н. Петрова А.В.",
                "tags": json.dumps(["аллергия", "укусы", "насекомые", "анафилаксия"], ensure_ascii=False)
            },
            {
                "title": "Практическое руководство по неотложной помощи при укусах насекомых",
                "description": "Пошаговые инструкции по оказанию первой помощи при укусах различных насекомых",
                "content": "Инструкции по первой помощи...",
                "category": "Неотложная помощь",
                "author": "Врач скорой помощи Сидоров С.С.",
                "tags": json.dumps(["первая помощь", "укусы", "неотложная помощь", "насекомые"], ensure_ascii=False)
            },
            {
                "title": "Кариес зубов: современные методы диагностики",
                "description": "Обзор современных методов выявления и классификации кариеса",
                "content": "Методы диагностики кариеса...",
                "category": "Стоматология",
                "author": "Стоматолог-терапевт Кузнецова О.М.",
                "tags": json.dumps(["зубы", "кариес", "диагностика", "стоматология"], ensure_ascii=False)
            },
            {
                "title": "Аллергология и иммунология",
                "description": "Основы аллергологии и клинической иммунологии",
                "content": "Базовые принципы аллергологии...",
                "category": "Аллергология",
                "author": "Профессор, д.м.н. Волков В.В.",
                "tags": json.dumps(["аллергия", "иммунология", "диагностика", "лечение"], ensure_ascii=False)
            }
        ]
        
        # Добавляем каждую статью в базу данных
        for data in literature_data:
            literature = Literature(**data)
            db.add(literature)
        
        db.commit()
        print("База данных успешно инициализирована тестовыми данными")
        
    except Exception as e:
        print(f"Ошибка при инициализации базы данных: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_database()

