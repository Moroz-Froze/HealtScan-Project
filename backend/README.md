# HealthScan Backend

Бэкэнд API для приложения медицинского сканирования ЗдравСкан.

## Функциональность

- **Аутентификация**: JWT токены, интеграция с Telegram Web App
- **Сканирование изображений**: Загрузка и анализ медицинских изображений
- **Система подписок**: Управление подписками пользователей (пробные и платные)
- **Справочная литература**: База знаний медицинской информации
- **История запросов**: Отслеживание активности пользователей

## Структура проекта

```
backend/
├── app.py                 # Главное приложение FastAPI
├── main.py               # Точка входа (совместимость)
├── database.py           # Настройка базы данных
├── models.py             # Модели SQLAlchemy
├── auth.py               # Аутентификация и авторизация
├── init_db.py            # Инициализация БД с тестовыми данными
├── routers/              # API роутеры
│   ├── auth_router.py    # Аутентификация
│   ├── scan_router.py    # Сканирование изображений
│   ├── subscription_router.py # Подписки
│   ├── literature_router.py   # Справочная литература
│   └── history_router.py      # История запросов
├── services/             # Бизнес-логика
│   └── image_analyzer.py # Анализ изображений
└── uploads/              # Загруженные файлы
```

## Установка и запуск

### 1. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 2. Настройка переменных окружения

Создайте файл `.env` в папке backend на основе `env_example.txt`:

```bash
SECRET_KEY=your-super-secret-key-here
BOT_TOKEN=your-telegram-bot-token
DATABASE_URL=sqlite:///./app.db
```

### 3. Инициализация базы данных

```bash
cd backend
python init_db.py
```

### 4. Запуск сервера

```bash
# Для разработки
python app.py

# Или через uvicorn
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

## API Endpoints

### Аутентификация
- `POST /api/auth/` - Аутентификация через Telegram
- `GET /api/auth/me` - Получение информации о пользователе

### Сканирование
- `POST /api/scan/upload` - Загрузка и анализ изображения
- `GET /api/scan/{scan_id}` - Получение результата сканирования
- `GET /api/scan/` - История сканирований

### Подписки
- `GET /api/subscription/status` - Статус подписки
- `POST /api/subscription/create` - Создание подписки
- `GET /api/subscription/plans` - Доступные планы

### Справочная литература
- `GET /api/literature/` - Список литературы
- `GET /api/literature/{id}` - Подробная информация
- `GET /api/literature/search/` - Поиск в литературе

### История
- `GET /api/history/` - История запросов
- `DELETE /api/history/{id}` - Удаление записи
- `DELETE /api/history/` - Очистка истории

## Модели данных

### User (Пользователь)
- id, telegram_id, first_name, last_name, username
- created_at, updated_at

### Subscription (Подписка)
- user_id, subscription_type, status, start_date, end_date
- is_trial, auto_renew

### Scan (Сканирование)
- user_id, image_path, status, condition_detected
- description, confidence, recommendations

### Literature (Литература)
- title, description, content, category
- author, tags, is_active

### QueryHistory (История запросов)
- user_id, query_text, scan_id, created_at

## Конфигурация

### Переменные окружения

- `SECRET_KEY` - Секретный ключ для JWT токенов
- `BOT_TOKEN` - Токен Telegram бота
- `DATABASE_URL` - URL подключения к базе данных
- `CORS_ORIGINS` - Разрешенные CORS домены

### База данных

По умолчанию используется SQLite. Для PostgreSQL измените DATABASE_URL:
```
DATABASE_URL=postgresql://username:password@localhost/healthscan_db
```

## Развертывание

### Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Heroku

1. Создайте `Procfile`:
```
web: uvicorn app:app --host 0.0.0.0 --port $PORT
```

2. Установите переменные окружения в настройках Heroku

## Безопасность

- JWT токены для аутентификации
- Валидация данных через Pydantic
- CORS настройки
- Проверка подписи Telegram WebApp
- Загрузка файлов с проверкой типа

## Тестирование

```bash
# Запуск тестов
pytest

# Проверка API документации
# Откройте http://localhost:8000/docs
```

## Мониторинг

- `/health` - Проверка состояния сервиса
- `/` - Информация о API
- `/docs` - Swagger документация
- `/redoc` - ReDoc документация

