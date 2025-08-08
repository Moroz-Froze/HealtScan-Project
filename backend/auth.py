# auth.py
import hashlib
import hmac
import json
from urllib.parse import parse_qsl
from datetime import datetime, timedelta
from typing import Optional
from jose import jwt
from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

def validate_telegram_data(init_data: str) -> Optional[dict]:
    try:
        params = dict(parse_qsl(init_data))
    except:
        return None

    hash_val = params.pop('hash', None)
    if not hash_val:
        return None

    data_check_arr = sorted(params.items())
    data_check_string = '\n'.join([f"{k}={v}" for k, v in data_check_arr])

    secret_key = hmac.new(b"WebAppBotToken", BOT_TOKEN.encode(), hashlib.sha256).digest()
    computed_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()

    if computed_hash != hash_val:
        return None

    user_str = params.get("user")
    if user_str:
        try:
            user_data = json.loads(user_str)
            return {
                "id": user_data["id"],
                "first_name": user_data.get("first_name", ""),
                "last_name": user_data.get("last_name", ""),
                "username": user_data.get("username", ""),
                "language_code": user_data.get("language_code", "en"),
            }
        except:
            return None
    return None

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)