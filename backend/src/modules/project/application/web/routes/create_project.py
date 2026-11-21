from fastapi import APIRouter, Depends, status

from src.modules.project.application.controllers.create_project_controller import (
    CreateProjectController,
)
from src.modules.project.application.usecases.create_project_usecase import (
    CreateProjectUsecase,
)
from src.modules.project.application.web.dependencies import (
    get_gateway_storage,
    get_repo_project,
)
from src.modules.project.application.web.schemas.create_project_schema import (
    CreateProjectRequestSchema,
    CreateProjectResponseSchema,
)

create_project_router = APIRouter()

def get_create_project_dependencies() -> CreateProjectController:
    repo = get_repo_project()
    gateway = get_gateway_storage()
    usecase = CreateProjectUsecase(
        repo=repo,
        gateway_storage=gateway
        )
    controller = CreateProjectController(usecase)

    return controller

@create_project_router.post(
    "/create",
    status_code=status.HTTP_201_CREATED,
    response_model=CreateProjectResponseSchema,
)
async def create_project(
    request: CreateProjectRequestSchema,
    controller: CreateProjectController = Depends(get_create_project_dependencies),
):
    return controller(request)