from database.basic_tools import AsyncBaseIdSQLAlchemyCRUD
from database.models.role_rules import RoleRuleModel
from asyncio import Lock


class RoleRuleTool(AsyncBaseIdSQLAlchemyCRUD):
    model = RoleRuleModel
    field_id = "id"
    lock: Lock = Lock()

