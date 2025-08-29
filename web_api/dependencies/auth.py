import datetime
from jose import jwt, JWTError, ExpiredSignatureError
from fastapi import Response
from typing import Optional, Dict, Any
import random
import string
import time


def create_jwt_token(user_id: int) -> str:
    """
    Создает JWT токен для пользователя
    
    Args:
        user_id: ID пользователя
        
    Returns:
        str: JWT токен
    """
    now = datetime.datetime.now(datetime.timezone.utc)
    now_timestamp = int(time.time())
    expiration = now + datetime.timedelta(seconds=60 * 60 * 24 * 7)
    expiration_timestamp = int(expiration.timestamp())
    session_id = "".join(random.choices(string.ascii_letters + string.digits, k=16))
    
    payload = {
        "jti": session_id,  # JWT ID (уникальный идентификатор токена/сессии)
        "sub": str(user_id),     # subject (ID пользователя) - должен быть строкой
        "iat": now_timestamp,          # issued at (время выдачи)
        "nbf": now_timestamp,          # not before (не действителен до)
        "exp": expiration_timestamp,   # expiration time (время истечения)
        "iss": "cryptoside.tech"       # issuer (издатель)
    }
    
    return jwt.encode(
        payload,
        "secret",
        algorithm="HS256"
    )


def set_auth_cookie(response: Response, user_id: int) -> None:
    """
    Устанавливает JWT токен в cookie
    
    Args:
        response: Объект ответа FastAPI
        user_id: ID пользователя
    """
    token = create_jwt_token(user_id)
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,  # Недоступен для JavaScript
        secure=True,    # Только по HTTPS
        samesite="lax", # Защита от CSRF
        max_age=60 * 60 * 24 * 7,
        path="/"
    )


def get_jwt_payload(token: str) -> Optional[Dict[str, Any]]:
    """
    Возвращает содержимое JWT токена
    
    Args:
        token: JWT токен для проверки
        
    Returns:
        dict: Содержимое токена или None, если токен недействителен
    """
    try:
        payload = jwt.decode(
            token, 
            "secret", 
            algorithms=["HS256"],
            options={
                "verify_signature": True,  # проверка подписи
                "verify_exp": True,        # проверка срока действия
                "verify_nbf": True,        # проверка "не ранее чем"
                "verify_iat": True,        # проверка времени выдачи
                "verify_aud": False,       # проверка аудитории (отключено)
                "require": ["exp", "iat", "nbf", "sub", "jti"]  # обязательные поля
            }
        )
        
        # Дополнительная проверка наличия sub и jti
        if "sub" not in payload or "jti" not in payload:
            return None
            
        # Проверка издателя
        if payload.get("iss") != "cryptoside.tech":
            return None
        
        payload["sub"] = int(payload["sub"])
        return payload
    except ExpiredSignatureError as ex_:
        return None
    except JWTError as ex_:
        return None
    except Exception as ex_:
        return None
