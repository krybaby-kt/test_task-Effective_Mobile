"""
Эндпоинты для управления пользователями.

Содержит маршруты для регистрации, входа, выхода, смены пароля и удаления аккаунта.
"""
from fastapi import APIRouter, Request, Depends, HTTPException, status
from typing import Annotated, Literal
from web_api.dependencies.cookies_auth import set_auth_cookie, get_jwt_payload
from database.tools.users import UserTool
from database.models.users import UserModel
from web_api.endpoints.users.schematics import SignUpRequest, SignUpResponse, SignInRequest, SignInResponse, SignOutResponse, ChangePasswordRequest, ChangePasswordResponse, DeleteAccountResponse
import string
from fastapi.responses import JSONResponse
from database.tools.sessions import SessionTool
from web_api.dependencies.users_auth import get_user

# Router для пользовательских операций
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
    """
    Регистрирует нового пользователя в системе.
    
    Создает новый аккаунт пользователя с автоматическим назначением роли "user",
    устанавливает JWT токен в cookies и создает сессию.
    
    Args:
        request: HTTP запрос
        user_data: Данные для регистрации (email, пароль)
        
    Returns:
        JSON ответ с результатом операции и установленным auth cookie
        
    Raises:
        HTTPException: 401 если email уже существует
    """
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
    """
    Аутентифицирует пользователя и создает сессию.
    
    Проверяет учетные данные, поддерживает миграцию паролей с SHA-256 на bcrypt,
    устанавливает JWT токен в cookies и создает новую сессию.
    
    Args:
        request: HTTP запрос
        user_data: Данные для входа (email, пароль)
        
    Returns:
        JSON ответ с результатом операции и установленным auth cookie
        
    Raises:
        HTTPException: 401 если неверные учетные данные или пользователь неактивен
    """
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
    """
    Завершает текущую сессию пользователя.
    
    Удаляет JWT токен из cookies, удаляет сессию из базы данных.
    
    Args:
        request: HTTP запрос с токеном в cookies
        dbUser: Текущий пользователь из dependency
        
    Returns:
        JSON ответ с результатом операции
        
    Raises:
        HTTPException: 401 если токен отсутствует
    """ 
    access_token = request.cookies.get("access_token")
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


@router.post(
    '/change-password',
    description="Сменить пароль",
    response_model=ChangePasswordResponse,
    response_model_exclude_none=True
)
async def web_api_change_password(
    request: Request,
    user_data: ChangePasswordRequest,
    dbUser: UserModel = Depends(get_user)
):
    """
    Изменяет пароль текущего пользователя.
    
    Проверяет старый пароль, обновляет на новый и завершает все остальные сессии
    пользователя, кроме текущей.
    
    Args:
        request: HTTP запрос с токеном в cookies
        user_data: Данные для смены пароля (старый и новый пароли)
        dbUser: Текущий пользователь из dependency
        
    Returns:
        JSON ответ с результатом операции
        
    Raises:
        HTTPException: 401 если токен отсутствует, 400 если неверный старый пароль
    """
    access_token = request.cookies.get("access_token")
    if not access_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Access token is required")
    
    if not await UserTool.verify_and_migrate_password(dbUser, user_data.old_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid email, username or password")
    
    await UserTool(dbUser.id).update(data={"password": UserTool.hash_password(user_data.new_password)})
    await SessionTool.delete_all_instead_of_current_user_id_and_access_token(user_id=dbUser.id, access_token=access_token)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=dict(
            success=True
        )
    )


@router.post(
    '/delete-account',
    description="Удалить аккаунт",
    response_model=DeleteAccountResponse,
    response_model_exclude_none=True
)
async def web_api_delete_account(
    request: Request,
    dbUser: UserModel = Depends(get_user)
):
    """
    Деактивирует аккаунт пользователя.
    
    Помечает пользователя как неактивного и удаляет все его сессии.
    Аккаунт становится недоступным для входа.
    
    Args:
        request: HTTP запрос
        dbUser: Текущий пользователь из dependency
        
    Returns:
        JSON ответ с результатом операции
    """
    await UserTool(dbUser.id).update(data=dict(is_active=False))
    await SessionTool.delete_all_by_user_id(user_id=dbUser.id)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=dict(
            success=True
        )
    )