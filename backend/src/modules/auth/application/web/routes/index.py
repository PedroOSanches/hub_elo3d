from fastapi import APIRouter
from src.modules.auth.application.web.routes.login_routes import login_router
from src.modules.auth.application.web.routes.refresh_route import refresh_router

auth_router = APIRouter()

auth_router.include_router(login_router)
auth_router.include_router(refresh_router)