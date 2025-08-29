"""
Модуль для проверки прав пользователя на основе ролей.
"""
from database.models.users import UserModel
from fastapi import Depends, HTTPException, status
from web_api.dependencies.users_auth import get_user
from database.tools.role_rules import RoleRuleTool
from database.models.role_rules import RoleRuleModel


def require_rule(rule: str):
    """
    Фабрика для создания dependency, которая проверяет наличие конкретного права у пользователя.
    
    Args:
        rule: Название права, необходимого для доступа
        
    Returns:
        FastAPI dependency для проверки права
        
    Raises:
        HTTPException: Если у пользователя нет необходимого права (403)
        
    Example:
        @router.get("/admin", dependencies=[require_rule("admin_access")])
        async def admin_endpoint():
            return {"message": "Admin content"}
    """
    async def rule_dependency(user: UserModel = Depends(get_user)):
        if not user or rule not in [dbRoleRule.rule_name for dbRoleRule in await RoleRuleTool.get_all_with_filters(filters=[RoleRuleModel.role_name == user.role])]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, 
                detail="Forbidden"
            )
    return Depends(rule_dependency)