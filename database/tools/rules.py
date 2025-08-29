"""
Инструменты для работы с моделью правил.

Обеспечивает базовые CRUD операции с правилами доступа.
"""
from database.basic_tools import AsyncBaseIdSQLAlchemyCRUD
from database.models.rules import RuleModel
from asyncio import Lock


class RuleTool(AsyncBaseIdSQLAlchemyCRUD):
    """
    Класс для управления правилами доступа.
    
    Наследует все базовые CRUD операции для работы с правилами.
    
    Attributes:
        model: Модель RuleModel
        field_id: Поле "name" как первичный ключ
        lock: Блокировка для потокобезопасной работы
    """
    model = RuleModel
    field_id = "name"
    lock: Lock = Lock()

