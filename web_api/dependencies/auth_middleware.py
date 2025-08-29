from fastapi import Request, status, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from web_api.dependencies.cookies_auth import get_jwt_payload


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path in ["/docs", "/redoc", "/openapi.json"]:
            return await call_next(request)
            
        access_token = request.cookies.get("access_token")
        
        if not access_token:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Access token required"}
            )
        
        payload = get_jwt_payload(access_token)
        if payload is None:
            response = JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Invalid or expired access token"}
            )
            response.delete_cookie(
                key="access_token",
                path="/",
                domain=None
            )
            return response
        
        response = await call_next(request)
        return response
