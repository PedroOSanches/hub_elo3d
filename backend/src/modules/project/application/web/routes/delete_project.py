from uuid import UUID
from fastapi import APIRouter, Depends, status, HTTPException

from src.modules.project.application.controllers.delete_project_controller import DeleteProjectController
from src.modules.project.application.usecases.delete_project_usecase import DeleteProjectUsecase
from src.modules.project.application.web.dependencies import get_repo_project
from src.modules.project.application.web.schemas.get_project_schema import GetProjectResponseSchema
from src.modules.project.domain.errors.project_errors import ProjectDeletionConflictError

delete_project_router = APIRouter()

def get_delete_project_dependencies() -> DeleteProjectController:
    repo = get_repo_project()
    usecase = DeleteProjectUsecase(repo)
    controller = DeleteProjectController(usecase)

    return controller

@delete_project_router.delete(
    "/delete/{project_id}",
    status_code=status.HTTP_200_OK,
    response_model=GetProjectResponseSchema
)
async def delete_project(
    project_id: UUID,
    controller: DeleteProjectController = Depends(get_delete_project_dependencies)):

    try:
        return controller(project_id)

    except ProjectDeletionConflictError as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(error)) from error