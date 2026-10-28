from uuid import UUID

from src.modules.printers.application.usecases.get_all_printers_by_user_usecase import (
    GetAllPrintersByUserUsecase,
)
from src.modules.printers.application.viewmodels.printer_viewmodel import (
    PrinterViewModel,
)
from src.modules.printers.application.web.schemas.printer_schema import (
    PrinterResponseSchema,
)


class GetAllPrintersByUserController:

    def __init__(self, usecase: GetAllPrintersByUserUsecase):
        self.usecase = usecase

    def __call__(self, user_id: UUID) -> list[PrinterResponseSchema]:
        printers = self.usecase(user_id)
        return PrinterViewModel.from_entities(printers)