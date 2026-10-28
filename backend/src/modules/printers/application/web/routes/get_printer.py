import uuid

from fastapi import APIRouter, status, Depends

from src.modules.printers.application.web.schemas.printer_schema import PrinterResponseSchema
from src.modules.printers.application.web.dependencies import get_repo_printer
from src.modules.printers.application.controllers.get_printer_controller import GetPrinterController
from src.modules.printers.application.usecases.get_printer_usecase import GetPrinterUsecase

get_router = APIRouter()


def get_get_printer_dependencies() -> GetPrinterController:
    repo = get_repo_printer()
    usecase = GetPrinterUsecase(repo_printer=repo)
    controller = GetPrinterController(usecase)
    return controller


@get_router.get(
    "/get/{printer_id}",
    status_code=status.HTTP_200_OK,
    response_model=PrinterResponseSchema,
)
async def get_printer(
    printer_id: uuid.UUID,
    controller: GetPrinterController = Depends(get_get_printer_dependencies),
):

    return controller(printer_id)