import uuid

from fastapi import APIRouter, status, Depends

from src.modules.printers.application.web.dependencies import get_repo_printer
from src.modules.printers.application.controllers.delete_printer_controller import DeletePrinterController
from src.modules.printers.application.usecases.delete_printer_usecase import DeletePrinterUsecase

delete_router = APIRouter()


def get_delete_printer_dependencies() -> DeletePrinterController:
    repo = get_repo_printer()
    usecase = DeletePrinterUsecase(repo_printer=repo)
    controller = DeletePrinterController(usecase)
    return controller


@delete_router.delete("/delete/{printer_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_printer(
    printer_id: uuid.UUID,
    controller: DeletePrinterController = Depends(get_delete_printer_dependencies),
):

    controller(printer_id)