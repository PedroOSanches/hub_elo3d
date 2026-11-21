from uuid import UUID

from src.modules.printers.domain.entities.printer import Printer
from src.modules.printers.domain.repositories.i_printer_repository import (
    IPrinterRepository,
)

AACD_ROLES = {"hospital", "user_hospital"}


class ListPrintersUsecase:

    def __init__(self, repo: IPrinterRepository):
        self.repo = repo

    def __call__(self, user_id: UUID, role: str) -> list[Printer]:
        if role in AACD_ROLES:
            return self.repo.get_all_printers()
        return self.repo.get_all_printers(user_id)