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

    @staticmethod
    async def get_by_role_name_and_rule_name(role_name: str, rule_name: str) -> RoleRuleModel:
        """
        Получает связь между ролью и правилом по именам.
        
        Ищет запись в таблице role_rules, которая связывает указанную роль и правило.
        Используется для проверки существования связи перед удалением или для валидации.
        
        Args:
            role_name: Имя роли для поиска
            rule_name: Имя правила для поиска
            
        Returns:
            Объект RoleRuleModel с найденной связью или None если связь не найдена
        """
        dbRoleRules: list[RoleRuleModel] = await RoleRuleTool.get_all_with_filters(filters=[RoleRuleModel.role_name == role_name, RoleRuleModel.rule_name == rule_name])
        if len(dbRoleRules) == 0:
            return None
        return dbRoleRules[0]

