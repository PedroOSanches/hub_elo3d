from typing import Any
from uuid import UUID

from src.modules.printers.domain.entities.printer import Printer
from src.modules.printers.domain.repositories.i_printer_repository import (
    IPrinterRepository,
)


class UpdatePrinterUsecase:

    def __init__(self, repo: IPrinterRepository):
        self.repo = repo

    def __call__(self, printer_id: UUID, data: dict[str, Any]) -> Printer:
        current = self.repo.get_printer(printer_id)
        updated = Printer(**{**current.model_dump(), **data})
        return self.repo.update_printer(printer_id, updated)