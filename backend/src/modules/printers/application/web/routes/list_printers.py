import uuid

from fastapi import APIRouter, status, Depends

from src.modules.printers.application.web.schemas.printer_schema import PrinterResponseSchema
from src.modules.printers.application.web.dependencies import get_repo_printer
from src.modules.printers.application.controllers.list_printers_controller import ListPrintersController
from src.modules.printers.application.usecases.list_printers_usecase import ListPrintersUsecase

list_router = APIRouter()


def get_list_printers_dependencies() -> ListPrintersController:
    repo = get_repo_printer()
    usecase = ListPrintersUsecase(repo_printer=repo)
    controller = ListPrintersController(usecase)
    return controller


@list_router.get(
    "/list",
    status_code=status.HTTP_200_OK,
    response_model=list[PrinterResponseSchema],
)
async def list_printers(
    usuario_id: uuid.UUID | None = None,
    controller: ListPrintersController = Depends(get_list_printers_dependencies),
):

    return controller(usuario_id)