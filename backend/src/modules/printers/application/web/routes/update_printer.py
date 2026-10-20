import uuid

from fastapi import APIRouter, status, Depends

from src.modules.printers.application.web.schemas.update_printer_schema import UpdatePrinterRequestSchema
from src.modules.printers.application.web.schemas.printer_schema import PrinterResponseSchema
from src.modules.printers.application.web.dependencies import get_repo_printer
from src.modules.printers.application.controllers.update_printer_controller import UpdatePrinterController
from src.modules.printers.application.usecases.update_printer_usecase import UpdatePrinterUsecase

update_router = APIRouter()


def get_update_printer_dependencies() -> UpdatePrinterController:
    repo = get_repo_printer()
    usecase = UpdatePrinterUsecase(repo_printer=repo)
    controller = UpdatePrinterController(usecase)
    return controller


@update_router.patch(
    "/update/{printer_id}",
    status_code=status.HTTP_200_OK,
    response_model=PrinterResponseSchema,
)
async def update_printer(
    printer_id: uuid.UUID,
    request: UpdatePrinterRequestSchema,
    controller: UpdatePrinterController = Depends(get_update_printer_dependencies),
):

    return controller(printer_id, request)