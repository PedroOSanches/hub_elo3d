from fastapi import APIRouter

from src.modules.project.application.web.routes.create_project import create_project_router
from src.modules.project.application.web.routes.get_project import get_project_router

project_router = APIRouter()

project_router.include_router(create_project_router)
project_router.include_router(get_project_router)