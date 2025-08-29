"""
Middleware для аутентификации пользователей через JWT токены в cookies.
"""
from fastapi import Request, status, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from web_api.dependencies.cookies_auth import get_jwt_payload
from database.tools.sessions import SessionTool


class AuthMiddleware(BaseHTTPMiddleware):
    """
    Middleware для проверки аутентификации пользователей.
    
    Проверяет наличие и валидность JWT токена в cookies для всех запросов,
    кроме публичных эндпоинтов (регистрация, вход, документация).
    """
    async def dispatch(self, request: Request, call_next):
        """
        Обрабатывает каждый HTTP запрос для проверки аутентификации.
        
        Args:
            request: HTTP запрос
            call_next: Следующий обработчик в цепочке middleware
            
        Returns:
            HTTP ответ с проверкой токена или ошибкой аутентификации
        """
        if request.url.path in ["/docs", "/redoc", "/openapi.json", "/users/sign-up", "/users/sign-in"]:
            return await call_next(request)
            
        access_token = request.cookies.get("access_token")
        
        if not access_token:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Access token required"}
            )
        
        payload = get_jwt_payload(access_token)
        if payload is None:
            response = JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Invalid or expired access token"}
            )
            response.delete_cookie(
                key="access_token",
                path="/",
                domain=None
            )
            return response
        elif not await SessionTool.get_by_user_id_and_access_token(user_id=payload.get("sub"), access_token=access_token):
            response = JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Expired access token"}
            )
            response.delete_cookie(
                key="access_token",
                path="/",
                domain=None
            )
            return response
        
        response = await call_next(request)
        return response
