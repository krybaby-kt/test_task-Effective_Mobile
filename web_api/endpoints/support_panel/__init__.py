from fastapi import APIRouter, Request, Depends, HTTPException, status
from web_api.dependencies.rules_auth import require_rule
from fastapi.responses import JSONResponse
from web_api.endpoints.support_panel.schematics import SupportPanelResponse


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
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=dict(
            success=True
        )
    )