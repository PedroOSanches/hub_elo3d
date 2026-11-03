from uuid import UUID
from fastapi import APIRouter, Depends, status

from src.modules.project.application.controllers.get_project_controller import GetProjectController
from src.modules.project.application.usecases.get_project_usecase import GetProjectUsecase
from src.modules.project.application.web.dependencies import get_repo_project
from src.modules.project.application.web.schemas.get_project_schema import GetProjectResponseSchema

get_project_router = APIRouter()

def get_get_project_dependencies() -> GetProjectController:
    repo = get_repo_project()
    usecase = GetProjectUsecase(repo)
    controller = GetProjectController(usecase)

    return controller

@get_project_router.get(
    "/get/{project_id}",
    status_code=status.HTTP_200_OK,
    response_model=GetProjectResponseSchema
)
async def get_project(
    project_id: UUID,
    controller: GetProjectController = Depends(get_get_project_dependencies)
):
    return controller(project_id)