from uuid import UUID

from src.modules.printers.domain.entities.printer import Printer
from src.modules.printers.domain.repositories.i_printer_repository import (
    IPrinterRepository,
)


class GetAllPrintersByUserUsecase:

    def __init__(self, repo_printer: IPrinterRepository):
        self.repo_printer = repo_printer

    def __call__(self, user_id: UUID) -> list[Printer]:
        return self.repo_printer.get_all_printers(user_id)