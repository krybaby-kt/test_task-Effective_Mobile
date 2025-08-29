"""
Эндпоинты панели пользователя.

Маршруты для пользовательского функционала. Все эндпоинты требуют право "user_panel".
"""
from fastapi import APIRouter, Request, Depends, HTTPException, status
from web_api.dependencies.rules_auth import require_rule
from fastapi.responses import JSONResponse
from web_api.endpoints.user_panel.schematics import UserPanelResponse

# Router для пользовательской панели с обязательной проверкой прав пользователя
router = APIRouter(dependencies=[require_rule("user_panel")])


@router.post(
    '/', 
    description="Панель пользователя",
    response_model=UserPanelResponse,
    response_model_exclude_none=True
)
async def web_api_user_panel(
    request: Request,
):
    """
    Основной эндпоинт пользовательской панели.
    
    Доступен только пользователям с правом "user_panel".
    Предоставляет доступ к основному пользовательскому функционалу.
    
    Args:
        request: HTTP запрос
        
    Returns:
        JSON ответ с подтверждением успешного доступа к панели
        
    Note:
        Автоматически проверяет права пользователя через require_rule dependency
    """
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=dict(
            success=True
        )
    )