from database.basic_tools import AsyncBaseIdSQLAlchemyCRUD
from database.models.sessions import SessionModel
from asyncio import Lock


class SessionTool(AsyncBaseIdSQLAlchemyCRUD):
    model = SessionModel
    field_id = "id"
    lock: Lock = Lock()

    @staticmethod
    async def get_by_user_id_and_access_token(user_id: int, access_token: str) -> SessionModel:
        dbSessions: list[SessionModel] = await SessionTool.get_all_with_filters(filters=[SessionModel.user_id == user_id, SessionModel.access_token == access_token])
        if len(dbSessions) == 0:
            return None
        return dbSessions[0]
