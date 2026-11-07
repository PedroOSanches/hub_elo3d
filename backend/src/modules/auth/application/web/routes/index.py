from fastapi import APIRouter
from src.modules.auth.application.web.routes.login_route import login_router
from src.modules.auth.application.web.routes.logout_route import logout_router
from src.modules.auth.application.web.routes.refresh_route import refresh_router
from src.modules.auth.application.web.routes.me_route import route_me

auth_router = APIRouter()

auth_router.include_router(login_router)
auth_router.include_router(route_me)
auth_router.include_router(logout_router)
auth_router.include_router(refresh_router)