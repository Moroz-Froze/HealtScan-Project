# backend/test_api.py
import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_health_check():
    """Тест проверки здоровья API"""
    print("🔍 Тестирование health check...")
    response = requests.get(f"{BASE_URL}/health")
    assert response.status_code == 200
    print("✅ Health check passed")
    return response.json()

def test_root_endpoint():
    """Тест корневого endpoint"""
    print("🔍 Тестирование root endpoint...")
    response = requests.get(f"{BASE_URL}/")
    assert response.status_code == 200
    print("✅ Root endpoint passed")
    return response.json()

def test_auth():
    """Тест аутентификации"""
    print("🔍 Тестирование аутентификации...")
    auth_data = {
        "initData": "user=%7B%22id%22%3A12345%2C%22first_name%22%3A%22Test%22%2C%22username%22%3A%22testuser%22%7D"
    }
    response = requests.post(f"{BASE_URL}/api/auth/", json=auth_data)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    print("✅ Authentication passed")
    return data["access_token"]

def test_subscription_plans():
    """Тест получения планов подписки"""
    print("🔍 Тестирование планов подписки...")
    response = requests.get(f"{BASE_URL}/api/subscription/plans")
    assert response.status_code == 200
    data = response.json()
    assert "plans" in data
    assert len(data["plans"]) > 0
    print("✅ Subscription plans passed")
    return data

def test_literature_list():
    """Тест получения списка литературы"""
    print("🔍 Тестирование списка литературы...")
    response = requests.get(f"{BASE_URL}/api/literature/")
    assert response.status_code == 200
    data = response.json()
    assert "literature" in data
    print("✅ Literature list passed")
    return data

def test_with_auth(token):
    """Тест endpoints требующих аутентификации"""
    headers = {"Authorization": f"Bearer {token}"}
    
    print("🔍 Тестирование /api/auth/me...")
    response = requests.get(f"{BASE_URL}/api/auth/me", headers=headers)
    assert response.status_code == 200
    print("✅ Auth me passed")
    
    print("🔍 Тестирование статуса подписки...")
    response = requests.get(f"{BASE_URL}/api/subscription/status", headers=headers)
    assert response.status_code == 200
    print("✅ Subscription status passed")
    
    print("🔍 Тестирование создания пробной подписки...")
    sub_data = {"subscription_type": "trial"}
    response = requests.post(f"{BASE_URL}/api/subscription/create", json=sub_data, headers=headers)
    # Может быть 200 (создана) или 400 (уже есть)
    assert response.status_code in [200, 400]
    print("✅ Subscription creation passed")
    
    print("🔍 Тестирование истории...")
    response = requests.get(f"{BASE_URL}/api/history/", headers=headers)
    assert response.status_code == 200
    print("✅ History passed")

def run_tests():
    """Запуск всех тестов"""
    print("🚀 Запуск тестов HealthScan API...\n")
    print("🌐 Фронтенд: https://moroz-froze-healtscan-project-cce0.twc1.net")
    print("🔧 Backend API: http://localhost:8000")
    print("=" * 60)
    
    try:
        # Базовые тесты без аутентификации
        test_health_check()
        test_root_endpoint()
        test_subscription_plans()
        test_literature_list()
        
        # Тест аутентификации
        token = test_auth()
        
        # Тесты с аутентификацией
        test_with_auth(token)
        
        print("\n" + "=" * 60)
        print("🎉 Все тесты прошли успешно!")
        print("✅ API полностью работоспособен")
        print("🌐 Фронтенд готов к работе с бэкэндом")
        print("📱 Откройте: https://moroz-froze-healtscan-project-cce0.twc1.net")
        
    except requests.exceptions.ConnectionError:
        print("❌ Ошибка подключения к серверу")
        print("Убедитесь, что сервер запущен:")
        print("   cd backend && python start_server.py")
    except AssertionError as e:
        print(f"❌ Тест провален: {e}")
    except Exception as e:
        print(f"❌ Неожиданная ошибка: {e}")

if __name__ == "__main__":
    run_tests()
