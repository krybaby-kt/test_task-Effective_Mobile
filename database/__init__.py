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


async def fill_database():
    return

    from database.tools.users import UserTool
    from database.tools.sessions import SessionTool
    from database.tools.roles import RoleTool
    from database.tools.rules import RuleTool

    if not await RuleTool.get_all():
        await RuleTool.create(data=dict(
            name="service_statistics",
            comment="User can see service statistics"
        ))
        await RuleTool.create(data=dict(
            name="admin_panel",
            comment="User can see admin panel"
        ))
    
    if not await RoleTool.get_all():
        await RoleTool.create(data=dict(
            name="admin",
            rules="service_statistics",
            comment="Admin role"
        ))
        await RoleTool.create(data=dict(
            name="support",
            rules="service_statistics",
            comment="User can see support data"
        ))
        await RoleTool.create(data=dict(
            name="user",
            rules="admin_panel",
            comment="User role"
        ))
    
    if not await UserTool.get_all():
        await UserTool.create(data=dict(
            email="admin@example.com",
            password="admin",
            role="admin",
            is_active=True
        ))