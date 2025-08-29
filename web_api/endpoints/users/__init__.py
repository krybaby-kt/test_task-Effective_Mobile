from fastapi import APIRouter, Request, Depends, HTTPException, status
from typing import Annotated, Literal
from web_api.dependencies.cookies_auth import set_auth_cookie, get_jwt_payload
from database.tools.users import UserTool
from database.models.users import UserModel
from web_api.endpoints.users.schematics import SignUpRequest, SignUpResponse, SignInRequest, SignInResponse, SignOutResponse
import string
from fastapi.responses import JSONResponse
from database.tools.sessions import SessionTool
from web_api.dependencies.users_auth import get_user


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
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Email already exists")
    
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
    await SessionTool(dbUser.id).create(data=dict(
        user_id=dbUser.id,
        access_token=access_token
    ))

    return response


@router.post(
    '/sign-in',
    description="Войти в систему",
    response_model=SignInResponse,
    response_model_exclude_none=True
)
async def web_api_sign_in(
    request: Request,
    user_data: SignInRequest
):
    if not user_data.email:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Email is required")
    
    if not user_data.password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Password is required")
    
    dbUser: UserModel = await UserTool.get_by_email(user_data.email)

    if not dbUser:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")

    if not await UserTool.verify_and_migrate_password(dbUser, user_data.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    
    if not dbUser.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not active")

    response = JSONResponse(
        status_code=status.HTTP_200_OK,
        content=dict(
            success=True
        )
    )
    access_token = set_auth_cookie(response=response, user_id=dbUser.id)
    await SessionTool(dbUser.id).create(data=dict(
        user_id=dbUser.id,
        access_token=access_token
    ))
    
    return response


@router.post(
    '/sign-out',
    description="Выйти из системы",
    response_model=SignOutResponse,
    response_model_exclude_none=True
)
async def web_api_sign_out(
    request: Request,
    dbUser: UserModel = Depends(get_user)
): 
    access_token = get_jwt_payload(request.cookies.get("access_token"))
    if not access_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Access token is required")

    response = JSONResponse(
        status_code=status.HTTP_200_OK,
        content=dict(
            success=True
        )
    )
    response.delete_cookie(key="access_token")
    await SessionTool.delete_by_user_id_and_access_token(user_id=dbUser.id, access_token=access_token)
    return response