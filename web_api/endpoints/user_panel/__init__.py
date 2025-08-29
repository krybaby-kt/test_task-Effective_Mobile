from fastapi import APIRouter, Request, Depends, HTTPException, status
from web_api.dependencies.rules_auth import require_rule
from fastapi.responses import JSONResponse
from web_api.endpoints.user_panel.schematics import UserPanelResponse


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
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=dict(
            success=True
        )
    )