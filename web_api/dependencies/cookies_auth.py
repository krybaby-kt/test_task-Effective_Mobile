"""
Модуль для работы с JWT токенами в cookies.

Предоставляет функции для создания, валидации и установки JWT токенов.
"""
import datetime
from jose import jwt, JWTError, ExpiredSignatureError
from fastapi import Response
from typing import Optional, Dict, Any
import random
import string
import time


def create_jwt_token(user_id: int) -> str:
    """
    Создает JWT токен для пользователя.
    
    Args:
        user_id: Идентификатор пользователя
        
    Returns:
        Подписанный JWT токен со сроком действия 7 дней
    """
    now = datetime.datetime.now(datetime.timezone.utc)
    now_timestamp = int(time.time())
    expiration = now + datetime.timedelta(seconds=60 * 60 * 24 * 7)
    expiration_timestamp = int(expiration.timestamp())
    session_id = "".join(random.choices(string.ascii_letters + string.digits, k=16))
    
    payload = {
        "jti": session_id,
        "sub": str(user_id),
        "iat": now_timestamp,
        "nbf": now_timestamp,
        "exp": expiration_timestamp,
    }
    
    return jwt.encode(
        payload,
        "secret",
        algorithm="HS256"
    )


def set_auth_cookie(response: Response, user_id: int) -> str:
    """
    Создает JWT токен и устанавливает его в секюрную cookie.
    
    Args:
        response: HTTP ответ для установки cookie
        user_id: Идентификатор пользователя
        
    Returns:
        Созданный токен
    """
    token = create_jwt_token(user_id)
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=60 * 60 * 24 * 7,
        path="/"
    )
    return token


def get_jwt_payload(token: str) -> Optional[Dict[str, Any]]:
    """
    Валидирует JWT токен и извлекает его payload.
    
    Args:
        token: JWT токен для валидации
        
    Returns:
        Словарь с payload токена или None если токен невалиден
    """
    try:
        payload = jwt.decode(
            token, 
            "secret", 
            algorithms=["HS256"],
            options={
                "verify_signature": True,
                "verify_exp": True,
                "verify_nbf": True,
                "verify_iat": True,
                "verify_aud": False,
                "require": ["exp", "iat", "nbf", "sub", "jti"]
            }
        )
        
        if "sub" not in payload or "jti" not in payload:
            return None
            
        payload["sub"] = int(payload["sub"])
        return payload
    except ExpiredSignatureError as ex_:
        return None
    except JWTError as ex_:
        return None
    except Exception as ex_:
        return None
