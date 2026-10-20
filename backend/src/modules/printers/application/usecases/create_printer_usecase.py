from uuid import UUID

from src.modules.printers.domain.entities.printer import Printer
from src.modules.printers.domain.errors.printer_errors import UserNotFoundError
from src.modules.printers.domain.gateways.i_user_gateway import IUserGateway
from src.modules.printers.domain.repositories.i_printer_repository import (
    IPrinterRepository,
)


class CreatePrinterUsecase:

    def __init__(self, repo: IPrinterRepository, user_gateway: IUserGateway):
        self.repo = repo
        self.user_gateway = user_gateway

    def __call__(
        self,
        apelido: str,
        modelo: str,
        tecnologia_impressao: str,
        usuario_id: UUID,
        filamentos_aceitos: list[UUID],
    ) -> Printer:
        if not self.user_gateway.exists(usuario_id):
            raise UserNotFoundError(usuario_id)

        printer = Printer(
            apelido=apelido,
            modelo=modelo,
            tecnologia_impressao=tecnologia_impressao,
            usuario_id=usuario_id,
            filamentos_aceitos=filamentos_aceitos,
        )

        return self.repo.create_printer(printer)