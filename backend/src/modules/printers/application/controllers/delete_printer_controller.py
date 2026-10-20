from uuid import UUID

from src.modules.printers.application.usecases.delete_printer_usecase import (
    DeletePrinterUsecase,
)


class DeletePrinterController:

    def __init__(self, usecase: DeletePrinterUsecase):
        self.usecase = usecase

    def __call__(self, printer_id: UUID) -> None:
        self.usecase(printer_id)