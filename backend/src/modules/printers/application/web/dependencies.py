from src.modules.printers.domain.gateways.i_user_gateway import IUserGateway
from src.modules.printers.domain.repositories.i_printer_repository import (
    IPrinterRepository,
)
from src.modules.printers.infra.external.gateways.user_gateway import UserGateway
from src.modules.printers.infra.repositories.printer_repository_mock import (
    PrinterRepositoryMock,
)

# Instância única: o repositório em memória guarda os dados dentro dele, precisa ser o mesmo obj em todas as requisições
_repo_printer = PrinterRepositoryMock()


def get_repo_printer() -> IPrinterRepository:
    return _repo_printer


def get_user_gateway() -> IUserGateway:
    return UserGateway()