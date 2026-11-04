from fastapi import APIRouter, Depends, status

from src.modules.project.application.controllers.get_all_projects_controller import GetAllProjectsController
from src.modules.project.application.usecases.get_all_projects_usecase import GetAllProjectsUsecase
from src.modules.project.application.web.dependencies import get_repo_project
from src.modules.project.application.web.schemas.get_all_projects_schema import GetAllProjectsResponseSchema

get_all_projects_router = APIRouter()

def get_get_all_projects_dependencies() -> GetAllProjectsController:
    repo = get_repo_project()
    usecase = GetAllProjectsUsecase(repo)
    controller = GetAllProjectsController(usecase)

    return controller

@get_all_projects_router.get(
    "/get_all",
    status_code=status.HTTP_200_OK,
    response_model=GetAllProjectsResponseSchema
)
async def get_all_projects(
    controller: GetAllProjectsController = Depends(get_get_all_projects_dependencies)
):
    return controller()