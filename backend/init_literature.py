# backend/init_literature.py
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Literature, User, Subscription, SubscriptionType, SubscriptionStatus
import json
from datetime import datetime, timedelta

def create_sample_literature():
    """Создание примеров справочной литературы"""
    
    literature_items = [
        {
            "title": "Справочник по клинической офтальмологии",
            "description": "Комплексное руководство по диагностике и лечению глазных заболеваний",
            "content": "Офтальмология - это медицинская специальность, занимающаяся диагностикой и лечением заболеваний глаз. В данном справочнике рассмотрены основные методы диагностики, современные подходы к лечению наиболее распространенных заболеваний глаз, включая катаракту, глаукому, заболевания сетчатки и роговицы.",
            "category": "Офтальмология",
            "tags": json.dumps(["глаза", "диагностика", "лечение", "офтальмология"], ensure_ascii=False),
            "author": "Проф. А.В. Петров"
        },
        {
            "title": "Инсектная аллергия: диагностика и лечение",
            "description": "Руководство по аллергическим реакциям на укусы насекомых",
            "content": "Инсектная аллергия - это аллергические реакции на укусы или ужаления насекомых. Наиболее часто встречаются реакции на укусы пчел, ос, муравьев, комаров и клещей. Симптомы могут варьироваться от местной реакции до анафилактического шока.",
            "category": "Аллергология",
            "tags": json.dumps(["аллергия", "насекомые", "укусы", "лечение"], ensure_ascii=False),
            "author": "Д-р М.С. Иванова"
        },
        {
            "title": "Практическое руководство по неотложной помощи при укусах насекомых",
            "description": "Алгоритмы первой помощи при укусах различных насекомых",
            "content": "При укусах насекомых важно быстро оценить тяжесть реакции и оказать соответствующую помощь. Местные реакции включают покраснение, отек и зуд. Системные реакции могут включать крапивницу, затруднение дыхания и анафилактический шок.",
            "category": "Неотложная помощь",
            "tags": json.dumps(["неотложная помощь", "укусы", "первая помощь"], ensure_ascii=False),
            "author": "Служба скорой помощи"
        },
        {
            "title": "Кариес зубов: современные методы диагностики",
            "description": "Современные подходы к диагностике кариеса",
            "content": "Кариес - это процесс деминерализации твердых тканей зуба под воздействием кислот, вырабатываемых бактериями. Ранняя диагностика кариеса позволяет предотвратить серьезные осложнения и сохранить зуб.",
            "category": "Стоматология",
            "tags": json.dumps(["кариес", "зубы", "диагностика", "стоматология"], ensure_ascii=False),
            "author": "Д-р К.П. Смирнов"
        },
        {
            "title": "Аллергология и иммунология",
            "description": "Основы аллергологии и клинической иммунологии",
            "content": "Аллергические заболевания становятся все более распространенными. Понимание механизмов развития аллергических реакций помогает в выборе правильной тактики лечения и профилактики.",
            "category": "Аллергология",
            "tags": json.dumps(["аллергия", "иммунология", "диагностика"], ensure_ascii=False),
            "author": "Проф. Н.В. Федорова"
        },
        {
            "title": "Дерматология: заболевания кожи",
            "description": "Справочник по основным кожным заболеваниям",
            "content": "Кожа - самый большой орган человеческого тела, выполняющий множество функций. Заболевания кожи могут быть как самостоятельными, так и проявлениями системных заболеваний.",
            "category": "Дерматология",
            "tags": json.dumps(["кожа", "дерматология", "заболевания"], ensure_ascii=False),
            "author": "Д-р Е.А. Козлова"
        }
    ]
    
    db = SessionLocal()
    try:
        # Проверяем, есть ли уже литература в базе
        existing = db.query(Literature).first()
        if existing:
            print("Literature already exists in database")
            return
            
        for item_data in literature_items:
            literature = Literature(**item_data)
            db.add(literature)
        
        db.commit()
        print(f"Created {len(literature_items)} literature items")
        
    except Exception as e:
        print(f"Error creating literature: {e}")
        db.rollback()
    finally:
        db.close()

def create_test_user_with_subscription():
    """Создание тестового пользователя с активной подпиской"""
    
    db = SessionLocal()
    try:
        # Проверяем, есть ли уже тестовый пользователь
        existing_user = db.query(User).filter(User.telegram_id == 12345).first()
        if existing_user:
            print("Test user already exists")
            return
            
        # Создаем тестового пользователя
        test_user = User(
            telegram_id=12345,
            first_name="Test",
            last_name="User",
            username="testuser"
        )
        db.add(test_user)
        db.commit()
        db.refresh(test_user)
        
        # Создаем активную подписку для тестового пользователя
        subscription = Subscription(
            user_id=test_user.id,
            subscription_type=SubscriptionType.ANNUAL,
            status=SubscriptionStatus.ACTIVE,
            start_date=datetime.utcnow(),
            end_date=datetime.utcnow() + timedelta(days=365),
            is_trial=False,
            auto_renew=True
        )
        db.add(subscription)
        db.commit()
        
        print(f"Created test user with ID {test_user.id} and active subscription")
        
    except Exception as e:
        print(f"Error creating test user: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("Initializing database with sample data...")
    create_sample_literature()
    create_test_user_with_subscription()
    print("Database initialization completed!") 