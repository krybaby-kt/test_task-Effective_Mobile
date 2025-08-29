"""
Инструменты для работы с моделью сессий пользователей.

Обеспечивает управление JWT токенами и отслеживание активных сессий.
"""
from database.basic_tools import AsyncBaseIdSQLAlchemyCRUD
from database.models.sessions import SessionModel
from asyncio import Lock


class SessionTool(AsyncBaseIdSQLAlchemyCRUD):
    """
    Класс для управления сессиями пользователей.
    
    Предоставляет методы для создания, поиска и удаления сессий
    на основе пользователя и access_token.
    
    Attributes:
        model: Модель SessionModel
        field_id: Поле "id" как первичный ключ
        lock: Блокировка для потокобезопасной работы
    """
    model = SessionModel
    field_id = "id"
    lock: Lock = Lock()

    @staticmethod
    async def get_by_user_id_and_access_token(user_id: int, access_token: str) -> SessionModel:
        """
        Получает сессию по ID пользователя и токену.
        
        Args:
            user_id: Идентификатор пользователя
            access_token: JWT токен
            
        Returns:
            Объект сессии или None если не найдена
        """
        dbSessions: list[SessionModel] = await SessionTool.get_all_with_filters(filters=[SessionModel.user_id == user_id, SessionModel.access_token == access_token])
        if len(dbSessions) == 0:
            return None
        return dbSessions[0]

    @staticmethod
    async def delete_by_user_id_and_access_token(user_id: int, access_token: str):
        """
        Удаляет конкретную сессию по ID пользователя и токену.
        
        Используется при выходе из системы.
        
        Args:
            user_id: Идентификатор пользователя
            access_token: JWT токен для удаления
        """
        await SessionTool.delete_with_filters(filters=[SessionModel.user_id == user_id, SessionModel.access_token == access_token])

    @staticmethod
    async def delete_all_instead_of_current_user_id_and_access_token(user_id: int, access_token: str):
        """
        Удаляет все сессии пользователя, кроме текущей.
        
        Используется при смене пароля для завершения всех
        остальных активных сессий.
        
        Args:
            user_id: Идентификатор пользователя
            access_token: Токен, который нужно оставить активным
        """
        await SessionTool.delete_with_filters(filters=[SessionModel.user_id == user_id, SessionModel.access_token != access_token])
    
    @staticmethod
    async def delete_all_by_user_id(user_id: int):
        """
        Удаляет все сессии пользователя.
        
        Используется при удалении аккаунта для полного завершения
        всех сессий пользователя.
        
        Args:
            user_id: Идентификатор пользователя
        """
        await SessionTool.delete_with_filters(filters=[SessionModel.user_id == user_id])