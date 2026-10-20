from fastapi import APIRouter
from src.modules.user.application.web.routes.create_user_route import create_router
from src.modules.user.application.web.routes.get_user_route import get_user_router

user_router = APIRouter(prefix='/user')



user_router.include_router(router=create_router)
user_router.include_router(router=get_user_router)