from uuid import UUID

from src.modules.printers.application.usecases.get_printer_usecase import (
    GetPrinterUsecase,
)
from src.modules.printers.application.viewmodels.printer_viewmodel import (
    PrinterViewModel,
)
from src.modules.printers.application.web.schemas.printer_schema import (
    PrinterResponseSchema,
)


class GetPrinterController:

    def __init__(self, usecase: GetPrinterUsecase):
        self.usecase = usecase

    def __call__(self, printer_id: UUID) -> PrinterResponseSchema:
        printer = self.usecase(printer_id)
        return PrinterViewModel.from_entity(printer)