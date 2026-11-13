from fastapi import APIRouter

from src.modules.filaments.application.web.routes.get_all_filaments import get_all_router
from src.modules.filaments.application.web.routes.get_filament import get_router

router = APIRouter()

router.include_router(router=get_router)
router.include_router(router=get_all_router)