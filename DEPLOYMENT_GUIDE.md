# 🚀 Полное руководство по запуску HealthScan

## 📋 Обзор проекта

**HealthScan** - медицинское приложение для анализа изображений с системой подписок и базой знаний.

- **Фронтенд:** https://moroz-froze-healtscan-project-cce0.twc1.net
- **Бэкэнд:** Локальный сервер (инструкция ниже)

## ⚡ Быстрый запуск (5 минут)

### Шаг 1: Подготовка окружения
```bash
# Переход в папку проекта
cd HealtScan-Project

# Установка Python зависимостей
cd backend
pip install -r requirements.txt
```

### Шаг 2: Инициализация базы данных
```bash
# Создание БД с тестовыми данными
python run_init_db.py
```

### Шаг 3: Запуск бэкэнда
```bash
# Запуск сервера
python start_server.py
```

✅ **Готово!** Сервер запущен на http://localhost:8000

### Шаг 4: Проверка работы
```bash
# Автоматическое тестирование API
python test_api.py
```

## 🌐 Доступные URL

| Сервис | URL | Описание |
|--------|-----|----------|
| **Фронтенд** | https://moroz-froze-healtscan-project-cce0.twc1.net | Веб-интерфейс приложения |
| **API Backend** | http://localhost:8000 | REST API сервер |
| **API Docs** | http://localhost:8000/docs | Swagger документация |
| **Health Check** | http://localhost:8000/health | Проверка состояния |

## 🔧 Настройка Telegram Bot (опционально)

### Для полной функциональности создайте Telegram бота:

1. **Создание бота:**
   ```
   1. Напишите @BotFather в Telegram
   2. Отправьте команду /newbot
   3. Следуйте инструкциям
   4. Получите токен бота
   ```

2. **Настройка токена:**
   ```bash
   # В файле backend/start_server.py замените:
   os.environ.setdefault("BOT_TOKEN", "YOUR_REAL_BOT_TOKEN_HERE")
   ```

3. **Настройка Web App:**
   ```
   1. Отправьте @BotFather команду /setmenubutton
   2. Выберите вашего бота
   3. Укажите URL: https://moroz-froze-healtscan-project-cce0.twc1.net
   ```

## 📱 Тестирование полного цикла

### 1. Откройте фронтенд
Перейдите на https://moroz-froze-healtscan-project-cce0.twc1.net

### 2. Проверьте основные функции:
- ✅ Главная страница загружается
- ✅ История запросов отображается
- ✅ Кнопки навигации работают
- ✅ Страница подписок доступна
- ✅ Справочная литература загружается

### 3. Проверьте интеграцию с бэкэндом:
```bash
# Проверка соединения
curl http://localhost:8000/health

# Проверка литературы
curl http://localhost:8000/api/literature/

# Проверка планов подписки
curl http://localhost:8000/api/subscription/plans
```

## 🏗️ Архитектура системы

```
┌─────────────────────────────────────┐
│           Пользователь              │
└─────────────┬───────────────────────┘
              │
┌─────────────▼───────────────────────┐
│         Фронтенд (React)            │
│  https://moroz-froze-healtscan-     │
│  project-cce0.twc1.net              │
└─────────────┬───────────────────────┘
              │ HTTP API calls
┌─────────────▼───────────────────────┐
│        Бэкэнд (FastAPI)             │
│     http://localhost:8000           │
├─────────────────────────────────────┤
│ • Аутентификация (JWT)              │
│ • Сканирование изображений          │
│ • Система подписок                  │
│ • База медицинских знаний           │
│ • История запросов                  │
└─────────────┬───────────────────────┘
              │
┌─────────────▼───────────────────────┐
│      База данных (SQLite)           │
│         app.db                      │
└─────────────────────────────────────┘
```

## 🔄 Рабочий процесс

### Обычное использование:
1. Пользователь открывает фронтенд
2. Фронтенд обращается к API для получения данных
3. Пользователь может просматривать литературу без авторизации
4. Для сканирования нужна аутентификация и подписка

### Полная функциональность (с Telegram Bot):
1. Пользователь открывает приложение через Telegram
2. Автоматическая аутентификация через WebApp
3. Доступны все функции включая сканирование

## 🐞 Решение проблем

### Проблема: CORS ошибки
**Решение:** Убедитесь, что бэкэнд запущен и в настройках CORS указан правильный домен фронтенда

### Проблема: 404 ошибки API
**Решение:** Проверьте что бэкэнд запущен на порту 8000:
```bash
curl http://localhost:8000/health
```

### Проблема: База данных не инициализирована
**Решение:** Запустите инициализацию:
```bash
python run_init_db.py
```

### Проблема: Порт 8000 занят
**Решение:** Остановите другие процессы или измените порт в start_server.py

## 📊 Мониторинг

### Проверка состояния системы:
```bash
# Здоровье API
curl http://localhost:8000/health

# Количество статей в базе
curl http://localhost:8000/api/literature/ | jq '.total'

# Доступные планы подписки
curl http://localhost:8000/api/subscription/plans | jq '.plans | length'
```

## 🚀 Развертывание в продакшене

### Для публичного доступа к API:

1. **Используйте gunicorn:**
   ```bash
   pip install gunicorn
   gunicorn -w 4 -k uvicorn.workers.UvicornWorker app:app --bind 0.0.0.0:8000
   ```

2. **Или через Docker:**
   ```dockerfile
   FROM python:3.11-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   COPY . .
   EXPOSE 8000
   CMD ["python", "start_server.py"]
   ```

3. **Настройте реверс-прокси (nginx):**
   ```nginx
   location /api/ {
       proxy_pass http://localhost:8000/api/;
       proxy_set_header Host $host;
       proxy_set_header X-Real-IP $remote_addr;
   }
   ```

## ✅ Контрольный список готовности

- [ ] Python 3.8+ установлен
- [ ] Зависимости установлены (`pip install -r requirements.txt`)
- [ ] База данных инициализирована (`python run_init_db.py`)
- [ ] Бэкэнд запущен (`python start_server.py`)
- [ ] API тесты проходят (`python test_api.py`)
- [ ] Фронтенд доступен (https://moroz-froze-healtscan-project-cce0.twc1.net)
- [ ] CORS настроен правильно
- [ ] Telegram Bot создан (опционально)

**🎉 Проект готов к использованию!**
