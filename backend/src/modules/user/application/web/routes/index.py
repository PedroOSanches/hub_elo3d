from fastapi import APIRouter
from src.modules.user.application.web.routes.create_user_route import create_router

router = APIRouter()


router.include_router(router=create_router)