from database.base import engine, Base
from database.models.roles import RoleModel
from database.models.rules import RuleModel
from database.models.users import UserModel
from database.models.role_rules import RoleRuleModel
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
    from database.tools.users import UserTool
    from database.tools.sessions import SessionTool
    from database.tools.roles import RoleTool
    from database.tools.rules import RuleTool
    from database.tools.role_rules import RoleRuleTool

    if not await RuleTool.get_all():
        await RuleTool.create(data=dict(
            name="admin_panel",
            comment="User can see admin panel"
        ))
        await RuleTool.create(data=dict(
            name="support_panel",
            comment="User can see support panel"
        ))
        await RuleTool.create(data=dict(
            name="user_panel",
            comment="User can see user panel"
        ))
    
    if not await RoleTool.get_all():
        await RoleTool.create(data=dict(
            name="admin",
            comment="Admin role"
        ))
        await RoleTool.create(data=dict(
            name="support",
            comment="Support role"
        ))
        await RoleTool.create(data=dict(
            name="user",
            comment="User role"
        ))
    
    if not await RoleRuleTool.get_all():
        await RoleRuleTool.create(data=dict(
            role_name="admin",
            rule_name="admin_panel"
        ))
        await RoleRuleTool.create(data=dict(
            role_name="admin",
            rule_name="support_panel"
        ))
        await RoleRuleTool.create(data=dict(
            role_name="admin",
            rule_name="user_panel"
        ))

        await RoleRuleTool.create(data=dict(
            role_name="support",
            rule_name="support_panel"
        ))
        await RoleRuleTool.create(data=dict(
            role_name="support",
            rule_name="user_panel"
        ))

        await RoleRuleTool.create(data=dict(
            role_name="user",
            rule_name="user_panel"
        ))

    if not await UserTool.get_all():
        await UserTool.create(data=dict(
            email="admin@example.com",
            password=UserTool.hash_password("admin"),
            role="admin",
            is_active=True
        ))
        await UserTool.create(data=dict(
            email="support@example.com",
            password=UserTool.hash_password("support"),
            role="support",
            is_active=True
        ))
        await UserTool.create(data=dict(
            email="user@example.com",
            password=UserTool.hash_password("user"),
            role="user",
            is_active=True
        ))