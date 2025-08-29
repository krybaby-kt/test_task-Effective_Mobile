"""
Главный модуль FastAPI приложения.

Конфигурирует веб-приложение с аутентификацией, CORS и эндпоинтами
для управления пользователями и различных панелей доступа.
"""
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from web_api.dependencies.auth_middleware import AuthMiddleware

from web_api.endpoints import users
from web_api.endpoints import user_panel
from web_api.endpoints import support_panel
from web_api.endpoints import admin_panel


# FastAPI приложение с конфигурацией API документации
app = FastAPI(
    title="Test Task Effective Mobile",
    description="Backend API for Test Task Effective Mobile",
    version="1.0.0",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"]
)
app.add_middleware(
    AuthMiddleware
)

app.include_router(users.router, prefix="/users")
app.include_router(user_panel.router, prefix="/user-panel")
app.include_router(support_panel.router, prefix="/support-panel")
app.include_router(admin_panel.router, prefix="/admin-panel")