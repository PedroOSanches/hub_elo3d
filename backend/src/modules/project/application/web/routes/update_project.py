from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status

from src.modules.project.application.controllers.update_project_controller import UpdateProjectController
from src.modules.project.application.usecases.update_project_usecase import UpdateProjectUsecase
from src.modules.project.application.web.dependencies import get_repo_project
from src.modules.project.application.web.schemas.update_project_schema import UpdateProjectRequestSchema, UpdateProjectResponseSchema
from src.modules.project.domain.errors.project_errors import ProjectStatusConflictError

update_project_router = APIRouter()

def get_update_project_dependencies() -> UpdateProjectController:
    repo_project = get_repo_project()
    usecase = UpdateProjectUsecase(repo_project)
    controller = UpdateProjectController(usecase)

    return controller

@update_project_router.patch("/update/{project_id}", status_code=status.HTTP_200_OK, response_model=UpdateProjectResponseSchema)
async def update_project(
    project_id: UUID,
    request: UpdateProjectRequestSchema,
    controller: UpdateProjectController = Depends(get_update_project_dependencies)
):
    try:
        return controller(project_id, request)

    except ProjectStatusConflictError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e)) from e