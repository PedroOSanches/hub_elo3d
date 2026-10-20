from uuid import UUID

from src.modules.printers.domain.entities.printer import Printer
from src.modules.printers.domain.repositories.i_printer_repository import (
    IPrinterRepository,
)


class GetPrinterUsecase:

    def __init__(self, repo: IPrinterRepository):
        self.repo = repo

    def __call__(self, printer_id: UUID) -> Printer:
        return self.repo.get_printer(printer_id)