from src.modules.project.domain.repositories.project_repository_interface import (
    IProjectRepository,
)
from src.modules.project.infra.external.gateways.gateway_storage import GatewayStorage
from src.modules.project.infra.external.gateways.gateway_storage_mock import (
    GatewayStorageMock,
)
from src.modules.project.infra.repositories.project_repository_mock import (
    ProjectRepositoryMock,
)
from src.shared.environments.environments import env

from src.shared.environments.environments import env

_project_repository = ProjectRepositoryMock()

def get_repo_project() -> IProjectRepository:
    return _project_repository


def get_gateway_storage():
    if env.stage == 'PROD':
        return GatewayStorage()
    else:
        return GatewayStorageMock()