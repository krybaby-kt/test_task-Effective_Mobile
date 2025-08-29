from fastapi import APIRouter, Request, Depends, HTTPException, status
from web_api.dependencies.rules_auth import require_rule
from fastapi.responses import JSONResponse
from web_api.endpoints.admin_panel.schematics import AdminPanelResponse


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
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=dict(
            success=True
        )
    )