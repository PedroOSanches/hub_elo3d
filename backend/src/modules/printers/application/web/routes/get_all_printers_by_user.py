import uuid

from fastapi import APIRouter, status, Depends

from src.modules.printers.application.web.schemas.printer_schema import PrinterResponseSchema
from src.modules.printers.application.web.dependencies import get_repo_printer
from src.modules.printers.application.controllers.get_all_printers_by_user_controller import GetAllPrintersByUserController
from src.modules.printers.application.usecases.get_all_printers_by_user_usecase import GetAllPrintersByUserUsecase

get_all_by_user_router = APIRouter()


def get_all_printers_by_user_dependencies() -> GetAllPrintersByUserController:
    repo = get_repo_printer()
    usecase = GetAllPrintersByUserUsecase(repo_printer=repo)
    controller = GetAllPrintersByUserController(usecase)
    return controller


@get_all_by_user_router.get(
    "/user/{usuario_id}",
    status_code=status.HTTP_200_OK,
    response_model=list[PrinterResponseSchema],
)
async def get_all_printers_by_user(
    usuario_id: uuid.UUID,
    controller: GetAllPrintersByUserController = Depends(get_all_printers_by_user_dependencies),
):

    return controller(usuario_id)