from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from web_api.dependencies.auth_middleware import AuthMiddleware


app = FastAPI(
    title="Test Task Effective Mobile",
    description="Backend API for Test Task Effective Mobile",
    version="1.0.0",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"]
)
app.add_middleware(
    AuthMiddleware
)