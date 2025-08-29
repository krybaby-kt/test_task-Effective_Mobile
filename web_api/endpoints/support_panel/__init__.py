"""
Эндпоинты панели поддержки.

Маршруты для операций службы поддержки. Все эндпоинты требуют право "support_panel".
"""
from fastapi import APIRouter, Request, Depends, HTTPException, status
from web_api.dependencies.rules_auth import require_rule
from fastapi.responses import JSONResponse
from web_api.endpoints.support_panel.schematics import SupportPanelResponse

# Router для панели поддержки с обязательной проверкой прав поддержки
router = APIRouter(dependencies=[require_rule("support_panel")])


@router.post(
    '/', 
    description="Панель поддержки",
    response_model=SupportPanelResponse,
    response_model_exclude_none=True
)
async def web_api_support_panel(
    request: Request,
):
    """
    Основной эндпоинт панели поддержки.
    
    Доступен только пользователям с правом "support_panel".
    Предоставляет доступ к функционалу службы поддержки.
    
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