from database.models.users import UserModel
from fastapi import Depends, HTTPException, status
from web_api.dependencies.users_auth import get_user
from database.tools.role_rules import RoleRuleTool
from database.models.role_rules import RoleRuleModel


def require_rule(rule: str):
    async def rule_dependency(user: UserModel = Depends(get_user)):
        if not user or rule not in [dbRoleRule.rule_name for dbRoleRule in await RoleRuleTool.get_all_with_filters(filters=[RoleRuleModel.role_name == user.role])]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, 
                detail="Forbidden"
            )
    return Depends(rule_dependency)