from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Request

from src.modules.project.application.controllers.update_project_controller import UpdateProjectController
from src.modules.project.application.usecases.update_project_usecase import UpdateProjectUsecase
from src.modules.project.application.web.dependencies import get_repo_project
from src.modules.project.application.web.schemas.update_project_schema import UpdateProjectRequestSchema, UpdateProjectResponseSchema
from src.modules.project.domain.errors.project_errors import ProjectStatusConflictError
from src.modules.user.domain.enums.role_enum import ROLE

update_project_router = APIRouter()

def get_update_project_dependencies() -> UpdateProjectController:
    repo_project = get_repo_project()
    usecase = UpdateProjectUsecase(repo_project)
    controller = UpdateProjectController(usecase)

    return controller

def get_current_user(request: Request) -> ROLE:
    current_user = getattr(request.state, "current_user", None)

    if not isinstance(current_user, dict):
        raise HTTPException(status_code=401, detail="Usuário não autenticado")

    try:
        return ROLE(current_user.get("role"))
    except (ValueError, TypeError):
        raise HTTPException(status_code=403, detail="Perfil inválido ou sem permissão")

@update_project_router.patch("/update/{project_id}", status_code=status.HTTP_200_OK, response_model=UpdateProjectResponseSchema)
async def update_project(
    project_id: UUID,
    request: UpdateProjectRequestSchema,
    controller: UpdateProjectController = Depends(get_update_project_dependencies),
    role: ROLE = Depends(get_current_user)
):
    data_roles = {ROLE.HOSPITAL, ROLE.USER_HOSPITAL}

    status_roles = {ROLE.HOSPITAL, ROLE.USER_HOSPITAL, ROLE.USER}

    has_data_changes = bool(request.model_fields_set - {"new_status"})

    has_status_change = request.new_status is not None

    if has_data_changes and role not in data_roles:
        raise HTTPException(status_code=403, detail="Perfil inválido ou sem permissão para alterar dados do projeto")

    if has_status_change and role not in status_roles:
        raise HTTPException(status_code=403, detail="Perfil inválido ou sem permissão para alterar status do projeto")
    
    try:
        return controller(project_id, request)

    except ProjectStatusConflictError as e:
        raise HTTPException(status_code=409, detail=str(e)) from e