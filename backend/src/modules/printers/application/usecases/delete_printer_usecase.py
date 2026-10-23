from uuid import UUID

from src.modules.printers.domain.repositories.i_printer_repository import (
    IPrinterRepository,
)


class DeletePrinterUsecase:

    def __init__(self, repo: IPrinterRepository):
        self.repo = repo

    def __call__(self, printer_id: UUID) -> None:
        self.repo.delete_printer(printer_id)