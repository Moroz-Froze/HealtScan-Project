# test.py
from auth import validate_telegram_data

# Пример initData (здесь hash сгенерирован НЕПРАВИЛЬНО — это просто заглушка)
# В реальности hash зависит от BOT_TOKEN и данных
init_data_example = (
    "query_id=AAEa6XZpAAAAADVpdmlf7vVxGQ&"
    "user=%7B%22id%22%3A123456789%2C%22first_name%22%3A%22Ivan%22%2C%22last_name%22%3A%22Ivanov%22%2C%22username%22%3A%22ivan95%22%2C%22language_code%22%3A%22ru%22%2C%22allows_write_to_pm%22%3Atrue%7D&"
    "auth_date=1712345678&"
    "hash=7a8e9f0e1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8"
)

result = validate_telegram_data(init_data_example)
print("Результат валидации:", result)

if result is None:
    print("❌ Ошибка: initData не прошёл проверку.")
    print("Возможные причины:")
    print("  1. Неверный BOT_TOKEN в .env")
    print("  2. Неверный hash (данные поддельные)")
    print("  3. Ошибка в синтаксисе или кодировке")
else:
    print("✅ Успех! Пользователь:", result)