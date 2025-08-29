from database.base import engine, Base
from database.models.roles import RoleModel
from database.models.rules import RuleModel
from database.models.users import UserModel
from database.models.sessions import SessionModel



async def init_models():
    """
    Инициализирует все модели базы данных.
    
    Создает все таблицы в базе данных на основе метаданных SQLAlchemy моделей.
    Функция безопасна для повторного вызова - не создает таблицы, которые уже существуют.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
