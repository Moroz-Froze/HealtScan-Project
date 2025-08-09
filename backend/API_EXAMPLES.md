# HealthScan API Examples

## Аутентификация

### 1. Вход через Telegram WebApp

```bash
curl -X POST "http://localhost:8000/api/auth/" \
  -H "Content-Type: application/json" \
  -d '{
    "initData": "user=%7B%22id%22%3A12345%2C%22first_name%22%3A%22Test%22%2C%22last_name%22%3A%22User%22%2C%22username%22%3A%22testuser%22%7D&auth_date=1234567890&hash=abc123"
  }'
```

**Ответ:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "telegram_id": 12345,
    "first_name": "Test",
    "last_name": "User",
    "username": "testuser"
  }
}
```

### 2. Получение информации о пользователе

```bash
curl -X GET "http://localhost:8000/api/auth/me" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## Сканирование изображений

### 3. Загрузка изображения для анализа

```bash
curl -X POST "http://localhost:8000/api/scan/upload" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -F "file=@path/to/medical_image.jpg"
```

**Ответ:**
```json
{
  "id": 1,
  "status": "processing",
  "created_at": "2024-01-15T10:30:00Z"
}
```

### 4. Получение результата анализа

```bash
curl -X GET "http://localhost:8000/api/scan/1" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

**Ответ:**
```json
{
  "id": 1,
  "status": "completed",
  "condition_detected": "Укус слепня",
  "description": "В большинстве случаев укус слепня для человека неприятен, но не опасен...",
  "confidence": 0.85,
  "recommendations": [
    "Промойте место укуса холодной водой",
    "Приложите лед для уменьшения отека",
    "Используйте антигистаминные препараты при аллергии"
  ],
  "created_at": "2024-01-15T10:30:00Z",
  "processed_at": "2024-01-15T10:32:15Z"
}
```

### 5. История сканирований

```bash
curl -X GET "http://localhost:8000/api/scan/?limit=10&offset=0" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## Подписки

### 6. Проверка статуса подписки

```bash
curl -X GET "http://localhost:8000/api/subscription/status" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

**Ответ:**
```json
{
  "has_active_subscription": true,
  "subscription": {
    "id": 1,
    "subscription_type": "trial",
    "status": "active",
    "start_date": "2024-01-15T10:00:00Z",
    "end_date": "2024-01-22T10:00:00Z",
    "is_trial": true,
    "days_remaining": 5,
    "auto_renew": false
  }
}
```

### 7. Создание пробной подписки

```bash
curl -X POST "http://localhost:8000/api/subscription/create" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "subscription_type": "trial"
  }'
```

### 8. Получение планов подписки

```bash
curl -X GET "http://localhost:8000/api/subscription/plans"
```

**Ответ:**
```json
{
  "plans": [
    {
      "type": "trial",
      "name": "Пробный период",
      "duration": "7 дней",
      "price": 0,
      "description": "Полный доступ ко всем функциям"
    },
    {
      "type": "express",
      "name": "Экспресс-проверка",
      "duration": "1 месяц",
      "price": 229,
      "description": "Подписка на 1 месяц"
    }
  ]
}
```

## Справочная литература

### 9. Список литературы

```bash
curl -X GET "http://localhost:8000/api/literature/?limit=10&offset=0"
```

**Ответ:**
```json
{
  "literature": [
    {
      "id": 1,
      "title": "Справочник по клинической офтальмологии",
      "description": "Полное руководство по диагностике и лечению заболеваний глаз",
      "category": "Офтальмология",
      "author": "Д.м.н. Иванов И.И.",
      "tags": ["глаза", "зрение", "конъюнктивит"]
    }
  ],
  "total": 5,
  "categories": ["Офтальмология", "Аллергология", "Стоматология"]
}
```

### 10. Получение конкретной статьи

```bash
curl -X GET "http://localhost:8000/api/literature/1" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### 11. Поиск в литературе

```bash
curl -X GET "http://localhost:8000/api/literature/search/?q=аллергия&limit=5"
```

### 12. Фильтрация по категории

```bash
curl -X GET "http://localhost:8000/api/literature/?category=Аллергология"
```

## История запросов

### 13. Получение истории

```bash
curl -X GET "http://localhost:8000/api/history/?limit=20&offset=0" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

**Ответ:**
```json
{
  "history": [
    {
      "id": 1,
      "query_text": "Укус слепня",
      "scan_id": 1,
      "created_at": "2024-01-15T10:32:15Z"
    },
    {
      "id": 2,
      "query_text": "Литература: Справочник по клинической офтальмологии",
      "scan_id": null,
      "created_at": "2024-01-15T09:15:00Z"
    }
  ],
  "total": 2
}
```

### 14. Удаление записи из истории

```bash
curl -X DELETE "http://localhost:8000/api/history/1" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### 15. Очистка всей истории

```bash
curl -X DELETE "http://localhost:8000/api/history/" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## Служебные endpoints

### 16. Проверка состояния сервиса

```bash
curl -X GET "http://localhost:8000/health"
```

**Ответ:**
```json
{
  "status": "healthy",
  "service": "healthscan-backend"
}
```

### 17. Информация об API

```bash
curl -X GET "http://localhost:8000/"
```

**Ответ:**
```json
{
  "message": "HealthScan Backend API",
  "version": "1.0.0",
  "docs": "/docs",
  "status": "running"
}
```

## Коды ошибок

### 401 - Unauthorized
```json
{
  "detail": "Could not validate credentials"
}
```

### 404 - Not Found
```json
{
  "error": "Not found",
  "message": "The requested resource was not found"
}
```

### 400 - Bad Request
```json
{
  "detail": "Invalid subscription type"
}
```

### 500 - Internal Server Error
```json
{
  "error": "Internal server error",
  "message": "Something went wrong"
}
```

## Примечания

1. Замените `YOUR_JWT_TOKEN` на реальный токен, полученный при аутентификации
2. Для загрузки файлов используйте `multipart/form-data`
3. Все временные метки в формате ISO 8601 UTC
4. API документация доступна по адресу `/docs` (Swagger UI)
5. Альтернативная документация доступна по адресу `/redoc`

