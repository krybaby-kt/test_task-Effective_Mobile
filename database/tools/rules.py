from database.basic_tools import AsyncBaseIdSQLAlchemyCRUD
from database.models.rules import RuleModel
from asyncio import Lock


class RuleTool(AsyncBaseIdSQLAlchemyCRUD):
    model = RuleModel
    field_id = "name"
    lock: Lock = Lock()

