# backend/services/image_analyzer.py
import random
import time
from typing import Dict, List
from PIL import Image
import os

# Симуляция медицинского анализа изображений
# В реальном проекте здесь была бы интеграция с ML моделью

MEDICAL_CONDITIONS = [
    {
        "condition": "Укус слепня",
        "description": "В большинстве случаев укус слепня для человека неприятен, но не опасен. Однако при склонности к аллергии или множественных укусах нужно обязательно обратиться к врачу.",
        "recommendations": [
            "Промойте место укуса холодной водой",
            "Приложите лед для уменьшения отека",
            "Используйте антигистаминные препараты при аллергии",
            "Обратитесь к врачу при сильной реакции"
        ],
        "confidence": 0.85
    },
    {
        "condition": "Укус комара",
        "description": "Укусы комаров обычно безвредны, но могут вызывать зуд и небольшой отек. В редких случаях могут передавать инфекции.",
        "recommendations": [
            "Не расчесывайте место укуса",
            "Приложите холодный компресс",
            "Используйте средства от зуда",
            "При множественных укусах обратитесь к врачу"
        ],
        "confidence": 0.92
    },
    {
        "condition": "Химический ожог",
        "description": "Химический ожог требует немедленного внимания. Степень серьезности зависит от типа химического вещества и времени воздействия.",
        "recommendations": [
            "Немедленно промойте пораженную область большим количеством воды",
            "Снимите загрязненную одежду",
            "Не используйте мази или домашние средства",
            "Обратитесь за медицинской помощью"
        ],
        "confidence": 0.78
    },
    {
        "condition": "Солнечный ожог",
        "description": "Солнечный ожог возникает при чрезмерном воздействии ультрафиолетовых лучей. Может варьироваться от легкого покраснения до серьезных повреждений кожи.",
        "recommendations": [
            "Приложите холодные компрессы к пораженной области",
            "Пейте много воды для предотвращения обезвоживания",
            "Используйте увлажняющие средства с алоэ вера",
            "При серьезных ожогах обратитесь к врачу"
        ],
        "confidence": 0.88
    },
    {
        "condition": "Аллергическая реакция",
        "description": "Аллергическая реакция на коже может проявляться в виде сыпи, покраснения, зуда или отека. Может быть вызвана различными аллергенами.",
        "recommendations": [
            "Определите и избегайте аллерген",
            "Примите антигистаминные препараты",
            "Используйте холодные компрессы для облегчения зуда",
            "При серьезных реакциях немедленно обратитесь к врачу"
        ],
        "confidence": 0.82
    },
    {
        "condition": "Царапина или порез",
        "description": "Небольшие царапины и порезы обычно заживают самостоятельно при правильном уходе. Важно предотвратить инфекцию.",
        "recommendations": [
            "Очистите рану мягким мылом и водой",
            "Нанесите антисептик",
            "Закройте рану стерильной повязкой",
            "Следите за признаками инфекции"
        ],
        "confidence": 0.95
    }
]

def analyze_medical_image(image_path: str) -> Dict:
    """
    Анализ медицинского изображения
    В реальном приложении здесь была бы ML модель
    """
    
    # Проверяем, что файл существует
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image file not found: {image_path}")
    
    # Симуляция времени обработки
    time.sleep(random.uniform(1, 3))
    
    try:
        # Загружаем изображение для проверки валидности
        with Image.open(image_path) as img:
            # Получаем размеры изображения для симуляции анализа
            width, height = img.size
            
            # Симуляция анализа на основе размера изображения
            # В реальности здесь была бы нейронная сеть
            condition_index = (width + height) % len(MEDICAL_CONDITIONS)
            
    except Exception as e:
        # Если не удалось открыть изображение, возвращаем случайный результат
        condition_index = random.randint(0, len(MEDICAL_CONDITIONS) - 1)
    
    # Выбираем случайное медицинское состояние для демонстрации
    selected_condition = MEDICAL_CONDITIONS[condition_index]
    
    # Добавляем небольшую случайность в уверенность
    confidence_variation = random.uniform(-0.1, 0.1)
    final_confidence = max(0.5, min(0.99, selected_condition["confidence"] + confidence_variation))
    
    return {
        "condition": selected_condition["condition"],
        "description": selected_condition["description"],
        "recommendations": selected_condition["recommendations"],
        "confidence": round(final_confidence, 2)
    }

def validate_medical_image(image_path: str) -> bool:
    """
    Проверка, подходит ли изображение для медицинского анализа
    """
    try:
        with Image.open(image_path) as img:
            # Проверяем минимальные требования к изображению
            width, height = img.size
            
            # Минимальное разрешение
            if width < 100 or height < 100:
                return False
            
            # Максимальное разрешение (для экономии ресурсов)
            if width > 4000 or height > 4000:
                return False
            
            # Проверяем формат
            if img.format not in ['JPEG', 'PNG', 'JPG']:
                return False
            
            return True
            
    except Exception:
        return False

def get_supported_conditions() -> List[str]:
    """
    Получение списка поддерживаемых медицинских состояний
    """
    return [condition["condition"] for condition in MEDICAL_CONDITIONS]

