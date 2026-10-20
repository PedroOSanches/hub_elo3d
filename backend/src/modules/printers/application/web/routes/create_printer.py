from fastapi import APIRouter, status, Depends

from src.modules.printers.application.web.schemas.create_printer_schema import CreatePrinterRequestSchema
from src.modules.printers.application.web.schemas.printer_schema import PrinterResponseSchema
from src.modules.printers.application.web.dependencies import get_repo_printer, get_user_gateway
from src.modules.printers.application.controllers.create_printer_controller import CreatePrinterController
from src.modules.printers.application.usecases.create_printer_usecase import CreatePrinterUsecase

create_router = APIRouter()


def get_create_printer_dependencies() -> CreatePrinterController:
    repo = get_repo_printer()
    user_gateway = get_user_gateway()
    usecase = CreatePrinterUsecase(repo_printer=repo, user_gateway=user_gateway)
    controller = CreatePrinterController(usecase)
    return controller


@create_router.post(
    "/create",
    status_code=status.HTTP_201_CREATED,
    response_model=PrinterResponseSchema,
)
async def create_printer(
    request: CreatePrinterRequestSchema,
    controller: CreatePrinterController = Depends(get_create_printer_dependencies),
):

    return controller(request)