# ЗдравСкан Backend

FastAPI бэкенд для медицинского приложения ЗдравСкан.

## Установка и запуск

### 1. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 2. Настройка окружения

Создайте файл `.env` в папке `backend`:

```env
# База данных
DATABASE_URL=sqlite:///./app.db

# JWT
SECRET_KEY=your-super-secret-key-change-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=10080

# Telegram Bot
BOT_TOKEN=YOUR_BOT_TOKEN_HERE

# Настройки приложения
DEBUG=True
```

### 3. Инициализация базы данных

```bash
python init_db.py
```

### 4. Запуск сервера

```bash
# Разработка
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Продакшн
uvicorn main:app --host 0.0.0.0 --port 8000
```

## API Endpoints

### Аутентификация
- `POST /api/auth` - Аутентификация через Telegram

### Сканирование
- `POST /api/scan` - Сканирование изображения (требует подписку)

### История
- `GET /api/history` - История сканирований пользователя

### Литература
- `GET /api/literature` - Список справочной литературы

### Подписка
- `POST /api/subscription` - Создание подписки

### Профиль
- `GET /api/user/profile` - Профиль пользователя

### Системные
- `GET /` - Информация об API
- `GET /health` - Проверка здоровья сервера

## Документация API

После запуска сервера документация доступна по адресу:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Структура проекта

```
backend/
├── main.py              # Основной файл приложения
├── config.py            # Конфигурация
├── auth.py              # Аутентификация (устаревший)
├── init_db.py           # Инициализация БД
├── requirements.txt     # Зависимости
├── README.md           # Документация
├── app.db              # База данных SQLite
└── uploads/            # Папка для загруженных изображений
```

## Модели базы данных

### User
- `id` - ID пользователя
- `telegram_id` - ID в Telegram
- `first_name` - Имя
- `last_name` - Фамилия
- `username` - Имя пользователя
- `subscription_expires` - Дата окончания подписки
- `is_subscribed` - Статус подписки

### ScanHistory
- `id` - ID записи
- `user_id` - ID пользователя
- `image_path` - Путь к изображению
- `result` - Результат анализа (JSON)
- `created_at` - Дата создания

### Literature
- `id` - ID записи
- `title` - Название
- `description` - Описание
- `file_path` - Путь к файлу
- `category` - Категория

## Безопасность

- Все эндпоинты (кроме `/api/auth`) требуют JWT токен
- Валидация данных от Telegram
- Проверка подписки для сканирования
- Ограничения на размер файлов

## Развертывание

### Локально
```bash
uvicorn main:app --reload
```

### Docker
```bash
docker build -t zdravscan-backend .
docker run -p 8000:8000 zdravscan-backend
```

### Vercel/Heroku
Настройте переменные окружения и запустите:
```bash
uvicorn main:app --host 0.0.0.0 --port $PORT
```
