# 🚀 Быстрый запуск HealthScan Backend

## 📋 Предварительные требования

- Python 3.8+
- pip

## ⚡ Быстрый запуск (3 шага)

### 1. Установка зависимостей
```bash
cd backend
pip install -r requirements.txt
```

### 2. Инициализация базы данных
```bash
python run_init_db.py
```

### 3. Запуск сервера
```bash
python app.py
```

Сервер будет доступен по адресу: **http://localhost:8000**

## 🧪 Проверка работоспособности

### Автоматический тест
```bash
python test_api.py
```

### Ручная проверка
- Откройте **http://localhost:8000** - должна отобразиться информация об API
- Откройте **http://localhost:8000/docs** - Swagger документация
- Откройте **http://localhost:8000/health** - проверка здоровья сервиса

## 📡 Основные endpoints

### Без аутентификации:
- `GET /` - Информация об API
- `GET /health` - Проверка здоровья
- `GET /docs` - Swagger документация
- `GET /api/subscription/plans` - Планы подписки
- `GET /api/literature/` - Список литературы
- `POST /api/auth/` - Аутентификация

### С аутентификацией:
- `GET /api/auth/me` - Информация о пользователе
- `POST /api/scan/upload` - Загрузка изображения
- `GET /api/subscription/status` - Статус подписки
- `POST /api/subscription/create` - Создание подписки

## 🔧 Настройка переменных окружения

Создайте файл `.env` на основе `env_example.txt`:

```bash
SECRET_KEY=your-secret-key-here
BOT_TOKEN=your-telegram-bot-token
DATABASE_URL=sqlite:///./app.db
```

## 🐞 Решение проблем

### Проблема: ModuleNotFoundError
**Решение:** Убедитесь, что находитесь в папке `backend` и установили зависимости

### Проблема: Database errors
**Решение:** Запустите `python run_init_db.py` для пересоздания БД

### Проблема: Port already in use
**Решение:** Измените порт в `app.py` или остановите другие процессы на порту 8000

## 📚 Дополнительная информация

- **Полная документация:** `README.md`
- **Примеры API:** `API_EXAMPLES.md`
- **Архитектура:** См. диаграмму в основном README

## ✅ Статус компонентов

- ✅ Аутентификация через Telegram WebApp
- ✅ Система подписок (пробная/платная)
- ✅ Загрузка и анализ изображений
- ✅ База медицинской литературы
- ✅ История запросов пользователей
- ✅ API документация (Swagger)
- ✅ Обработка ошибок
- ✅ CORS настройки
- ✅ Валидация данных

**Бэкэнд полностью готов к работе! 🎉**
