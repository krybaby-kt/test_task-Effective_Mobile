"""
Модуль для получения текущего пользователя из JWT токена.
"""
from fastapi import Cookie
from typing import Annotated, Union
from database.tools.users import UserTool
from web_api.dependencies.cookies_auth import get_jwt_payload
from database.models.users import UserModel


async def get_user(
    access_token: Annotated[str | None, Cookie(alias="access_token")] = None,
) -> Union[UserModel, None]:
    """
    Получает текущего аутентифицированного пользователя из JWT токена в cookies.
    
    Args:
        access_token: JWT токен из cookies браузера
        
    Returns:
        Объект пользователя или None если токен невалиден
        
    Note:
        Используется как dependency в FastAPI эндпоинтах для получения
        текущего пользователя после прохождения middleware аутентификации.
    """
    if payload_temp := get_jwt_payload(access_token):
        return await UserTool(payload_temp["sub"]).get()
    return None