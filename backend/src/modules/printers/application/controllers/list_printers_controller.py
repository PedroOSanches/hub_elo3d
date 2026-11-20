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
from src.modules.user.domain.enums.role_enum import ROLE


class ListPrintersController:

    def __init__(self, usecase: ListPrintersUsecase):
        self.usecase = usecase

    def __call__(self, user_id: UUID, role: ROLE) -> list[PrinterResponseSchema]:
        printers = self.usecase(user_id, role)
        return PrinterViewModel.from_entities(printers)