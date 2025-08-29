from fastapi import FastAPI, Request, status
from starlette.middleware.cors import CORSMiddleware
from fastapi.responses import Response
# from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware


app = FastAPI(
    title="Test Task Effective Mobile",
    description="Backend API for Test Task Effective Mobile",
    version="1.0.0",
    # docs_url=None,
    # redoc_url=None,
    # openapi_url=None
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"]
)
# app.add_middleware(HTTPSRedirectMiddleware)


@app.api_route("/{path_name:path}", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "HEAD", "PATCH", "TRACE"], include_in_schema=False)
async def catch_all(request: Request, path_name: str):
    return Response(status_code=status.HTTP_404_NOT_FOUND)
