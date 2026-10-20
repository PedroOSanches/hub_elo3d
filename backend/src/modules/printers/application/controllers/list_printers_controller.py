from uuid import UUID

from src.modules.printers.application.usecases.list_printers_usecase import (
    ListPrintersUsecase,
)
from src.modules.printers.application.viewmodels.printer_viewmodel import (
    PrinterViewModel,
)
from src.modules.printers.application.web.schemas.printer_schema import (
    PrinterResponseSchema,
)


class ListPrintersController:

    def __init__(self, usecase: ListPrintersUsecase):
        self.usecase = usecase

    def __call__(self, usuario_id: UUID | None = None) -> list[PrinterResponseSchema]:
        printers = self.usecase(usuario_id)
        return PrinterViewModel.from_entities(printers)