from database.basic_tools import AsyncBaseIdSQLAlchemyCRUD
from database.models.sessions import SessionModel
from asyncio import Lock


class SessionTool(AsyncBaseIdSQLAlchemyCRUD):
    model = SessionModel
    field_id = "user_id"
    lock: Lock = Lock()

