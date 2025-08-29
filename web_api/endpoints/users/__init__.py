from fastapi import APIRouter, Request, Depends, HTTPException, status
from typing import Annotated, Literal
from web_api.dependencies.users_auth import get_auth_type
from web_api.dependencies.cookies_auth import set_auth_cookie
from database.tools.users import UserTool
from database.models.users import UserModel
from web_api.endpoints.users.schematics import SignUpRequest, SignUpResponse
import string
from fastapi.responses import JSONResponse


router = APIRouter()


@router.post(
    '/sign-up', 
    description="Зарегистрироваться",
    response_model=SignUpResponse,
    response_model_exclude_none=True
)
async def web_api_sign_up(
    request: Request,
    user_data: SignUpRequest
):
    if await UserTool.get_by_email(user_data.email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")
    
    async with UserTool.lock:
        user_id: int = await UserTool.generate_unique_field_id(string.digits, length=12, return_type=int)
        dbUser: UserModel = await UserTool.create(data=dict(
                id=user_id,
                email=user_data.email,
                password=UserTool.hash_password(user_data.password),
                role="user",
                is_active=True
            )
        )
    
    response = JSONResponse(
        status_code=status.HTTP_200_OK,
        content=dict(
            success=True
        )
    )
    access_token = set_auth_cookie(response=response, user_id=dbUser.id)
    
    return response