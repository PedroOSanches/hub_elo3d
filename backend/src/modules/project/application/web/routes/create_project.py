from fastapi import APIRouter, Depends, Request, status

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
from src.shared.errors.usecase_error import ForbiddenAction

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
    request: Request,
    body: CreateProjectRequestSchema,
    controller: CreateProjectController = Depends(get_create_project_dependencies),
):
    current_user = request.state.current_user

    if current_user['role'] not in ['hospital', 'user_hospital']:
        raise ForbiddenAction("You don't have permission to create projects.")
    
    return controller(body)