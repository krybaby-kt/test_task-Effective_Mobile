"""
Инструменты для работы с моделью ролей.

Обеспечивает базовые CRUD операции с ролями пользователей.
"""
from database.basic_tools import AsyncBaseIdSQLAlchemyCRUD
from database.models.roles import RoleModel
from asyncio import Lock


class RoleTool(AsyncBaseIdSQLAlchemyCRUD):
    """
    Класс для управления ролями пользователей.
    
    Наследует все базовые CRUD операции для работы с ролями.
    
    Attributes:
        model: Модель RoleModel
        field_id: Поле "name" как первичный ключ
        lock: Блокировка для потокобезопасной работы
    """
    model = RoleModel
    field_id = "name"
    lock: Lock = Lock()

