from fastapi import APIRouter
from src.modules.auth.application.web.routes.login_routes import login_router


auth_router = APIRouter()

auth_router.include_router(login_router)