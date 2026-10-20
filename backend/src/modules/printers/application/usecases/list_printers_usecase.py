from uuid import UUID

from src.modules.printers.domain.entities.printer import Printer
from src.modules.printers.domain.repositories.i_printer_repository import (
    IPrinterRepository,
)


class ListPrintersUsecase:

    def __init__(self, repo: IPrinterRepository):
        self.repo = repo

    def __call__(self, usuario_id: UUID | None = None) -> list[Printer]:
        return self.repo.get_all_printers(usuario_id)
    