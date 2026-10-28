from fastapi import APIRouter

from src.modules.printers.application.web.routes.create_printer import create_router
from src.modules.printers.application.web.routes.get_printer import get_router
from src.modules.printers.application.web.routes.list_printers import list_router
from src.modules.printers.application.web.routes.update_printer import update_router
from src.modules.printers.application.web.routes.delete_printer import delete_router

router = APIRouter()

router.include_router(create_router)
router.include_router(get_router)
router.include_router(list_router)
router.include_router(update_router)
router.include_router(delete_router)