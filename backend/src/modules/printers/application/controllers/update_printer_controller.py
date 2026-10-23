from uuid import UUID

from src.modules.printers.application.usecases.update_printer_usecase import (
    UpdatePrinterUsecase,
)
from src.modules.printers.application.viewmodels.printer_viewmodel import (
    PrinterViewModel,
)
from src.modules.printers.application.web.schemas.printer_schema import (
    PrinterResponseSchema,
)
from src.modules.printers.application.web.schemas.update_printer_schema import (
    UpdatePrinterRequestSchema,
)


class UpdatePrinterController:

    def __init__(self, usecase: UpdatePrinterUsecase):
        self.usecase = usecase

    def __call__(
        self, printer_id: UUID, request: UpdatePrinterRequestSchema
    ) -> PrinterResponseSchema:
        data = request.model_dump(exclude_none=True)
        printer = self.usecase(printer_id, data)
        return PrinterViewModel.from_entity(printer)