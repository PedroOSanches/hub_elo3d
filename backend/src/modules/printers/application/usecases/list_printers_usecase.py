from uuid import UUID

from src.modules.printers.domain.entities.printer import Printer
from src.modules.printers.domain.repositories.i_printer_repository import (
    IPrinterRepository,
)
from src.modules.user.domain.enums.role_enum import ROLE

AACD_ROLES = {ROLE.HOSPITAL, ROLE.USER_HOSPITAL}


class ListPrintersUsecase:

    def __init__(self, repo: IPrinterRepository):
        self.repo = repo

    def __call__(self, user_id: UUID, role: ROLE) -> list[Printer]:
        # AACD vê todas, usuário comum só as próprias
        if role in AACD_ROLES:
            return self.repo.get_all_printers()
        return self.repo.get_all_printers(user_id)