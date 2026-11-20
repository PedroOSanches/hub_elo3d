from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Request, status

from src.modules.printers.application.controllers.list_printers_controller import (
    ListPrintersController,
)
from src.modules.printers.application.usecases.list_printers_usecase import (
    ListPrintersUsecase,
)
from src.modules.printers.application.web.dependencies import get_repo_printer
from src.modules.printers.application.web.schemas.printer_schema import (
    PrinterResponseSchema,
)
from src.modules.user.domain.enums.role_enum import ROLE

list_router = APIRouter()


def get_list_printers_dependencies() -> ListPrintersController:
    repo = get_repo_printer()
    usecase = ListPrintersUsecase(repo=repo)
    controller = ListPrintersController(usecase)
    return controller


def get_current_user(request: Request) -> tuple[UUID, ROLE]:
    current_user = getattr(request.state, "current_user", None)

    if not isinstance(current_user, dict):
        raise HTTPException(status_code=401, detail="Usuário não autenticado")

    try:
        return UUID(current_user["user_id"]), ROLE(current_user["role"])
    except (KeyError, ValueError, TypeError):
        raise HTTPException(
            status_code=403, detail="Perfil inválido ou sem permissão"
        ) from None


@list_router.get(
    "/list",
    status_code=status.HTTP_200_OK,
    response_model=list[PrinterResponseSchema],
)
async def list_printers(
    controller: ListPrintersController = Depends(get_list_printers_dependencies),
    current_user: tuple[UUID, ROLE] = Depends(get_current_user),
):
    user_id, role = current_user
    return controller(user_id, role)