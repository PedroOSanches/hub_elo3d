from fastapi import APIRouter

from src.modules.project.application.web.routes.create_project import create_project_router
from src.modules.project.application.web.routes.get_project import get_project_router
from src.modules.project.application.web.routes.get_all_projects import get_all_projects_router
from src.modules.project.application.web.routes.update_project import update_project_router
from src.modules.project.application.web.routes.delete_project import delete_project_router

project_router = APIRouter()

project_router.include_router(create_project_router)
project_router.include_router(get_project_router)
project_router.include_router(get_all_projects_router)
project_router.include_router(update_project_router)
project_router.include_router(delete_project_router)