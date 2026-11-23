from src.modules.printers.domain.gateways.i_user_gateway import IUserGateway
from src.modules.printers.domain.repositories.i_printer_repository import (
    IPrinterRepository,
)
from src.modules.printers.infra.external.gateways.user_gateway import UserGateway
from src.modules.printers.infra.repositories.printer_repository_mock import (
    PrinterRepositoryMock,
)
from src.modules.printers.infra.repositories.printer_repository_neo import (
    PrinterRepositoryNeo,
)
from src.shared.environments.environments import STAGE, env
from src.shared.environments.neo4j_connection_factory import connection

_repo_printer = PrinterRepositoryMock()


def get_repo_printer() -> IPrinterRepository:
    if env.stage == STAGE.PROD:
        return PrinterRepositoryNeo(connection=connection)

    return _repo_printer


def get_user_gateway() -> IUserGateway:
    return UserGateway()