"""
Инструменты для работы с моделью связей ролей и правил.

Обеспечивает управление отношениями Many-to-Many между ролями и правами.
"""
from database.basic_tools import AsyncBaseIdSQLAlchemyCRUD
from database.models.role_rules import RoleRuleModel
from asyncio import Lock


class RoleRuleTool(AsyncBaseIdSQLAlchemyCRUD):
    """
    Класс для управления связями между ролями и правилами.
    
    Позволяет создавать и удалять связи, а также получать списки
    правил для конкретных ролей.
    
    Attributes:
        model: Модель RoleRuleModel
        field_id: Поле "id" как первичный ключ
        lock: Блокировка для потокобезопасной работы
    """
    model = RoleRuleModel
    field_id = "id"
    lock: Lock = Lock()

