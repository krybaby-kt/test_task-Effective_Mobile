"""
Эндпоинты панели администратора.

Маршруты для административных операций. Все эндпоинты требуют право "admin_panel".
"""
from fastapi import APIRouter, Request, Depends, HTTPException, status
from web_api.dependencies.rules_auth import require_rule
from fastapi.responses import JSONResponse
from web_api.endpoints.admin_panel.schematics import AdminPanelResponse

# Router для административной панели с обязательной проверкой прав админа
router = APIRouter(dependencies=[require_rule("admin_panel")])


@router.post(
    '/', 
    description="Панель администратора",
    response_model=AdminPanelResponse,
    response_model_exclude_none=True
)
async def web_api_admin_panel(
    request: Request,
):
    """
    Основной эндпоинт административной панели.
    
    Доступен только пользователям с правом "admin_panel".
    Предоставляет доступ к административному функционалу.
    
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