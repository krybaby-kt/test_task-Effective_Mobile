from database.models.users import UserModel
from fastapi import Depends, HTTPException, status
from web_api.dependencies.users_auth import get_user


def require_rule(rule: str):
    async def rule_dependency(user: UserModel = Depends(get_user)):
        if not user or rule not in user.role.rules:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, 
                detail="Forbidden"
            )
    return Depends(rule_dependency)