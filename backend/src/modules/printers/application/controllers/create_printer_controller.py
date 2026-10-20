from src.modules.printers.application.usecases.create_printer_usecase import (
    CreatePrinterUsecase,
)
from src.modules.printers.application.viewmodels.printer_viewmodel import (
    PrinterViewModel,
)
from src.modules.printers.application.web.schemas.create_printer_schema import (
    CreatePrinterRequestSchema,
)
from src.modules.printers.application.web.schemas.printer_schema import (
    PrinterResponseSchema,
)


class CreatePrinterController:

    def __init__(self, usecase: CreatePrinterUsecase):
        self.usecase = usecase

    def __call__(self, request: CreatePrinterRequestSchema) -> PrinterResponseSchema:
        printer = self.usecase(**request.model_dump())
        return PrinterViewModel.from_entity(printer)