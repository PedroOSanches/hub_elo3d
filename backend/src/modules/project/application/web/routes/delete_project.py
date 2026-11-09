from uuid import UUID
from fastapi import APIRouter, Depends, status, HTTPException, Request

from src.modules.project.application.controllers.delete_project_controller import DeleteProjectController
from src.modules.project.application.usecases.delete_project_usecase import DeleteProjectUsecase
from src.modules.project.application.web.dependencies import get_repo_project
from src.modules.project.application.web.schemas.get_project_schema import GetProjectResponseSchema
from src.modules.project.domain.errors.project_errors import ProjectDeletionConflictError
from src.modules.user.domain.enums.role_enum import ROLE

delete_project_router = APIRouter()

def get_delete_project_dependencies() -> DeleteProjectController:
    repo = get_repo_project()
    usecase = DeleteProjectUsecase(repo)
    controller = DeleteProjectController(usecase)

    return controller

def get_delete_project_role(request: Request) -> ROLE:
    current_user = getattr(request.state, "current_user", None)

    if not isinstance(current_user, dict):
        raise HTTPException(status_code=401, detail="Usuário não autenticado")

    try:
        return ROLE(current_user.get("role"))
    except (ValueError, TypeError):
        raise HTTPException(status_code=403, detail="Perfil inválido ou sem permissão") from None

@delete_project_router.delete(
    "/delete/{project_id}",
    status_code=status.HTTP_200_OK,
    response_model=GetProjectResponseSchema
)
async def delete_project(
    project_id: UUID,
    controller: DeleteProjectController = Depends(
        get_delete_project_dependencies
    ),
    role: ROLE = Depends(get_delete_project_role)
):
    allowed_roles = {ROLE.HOSPITAL, ROLE.USER_HOSPITAL}

    if role not in allowed_roles:
        raise HTTPException(status_code=403, detail="Sem permissão para excluir projetos")

    try:
        return controller(project_id)

    except ProjectDeletionConflictError as error:
        raise HTTPException(status_code=409, detail=str(error)) from error