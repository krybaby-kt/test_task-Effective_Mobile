from database.basic_tools import AsyncBaseIdSQLAlchemyCRUD
from database.models.roles import RoleModel
from asyncio import Lock


class RoleTool(AsyncBaseIdSQLAlchemyCRUD):
    model = RoleModel
    field_id = "name"
    lock: Lock = Lock()

