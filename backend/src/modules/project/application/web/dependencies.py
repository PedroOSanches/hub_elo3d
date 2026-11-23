from src.modules.project.domain.repositories.project_repository_interface import (
    IProjectRepository,
)
from src.modules.project.infra.external.gateways.gateway_storage import (
    GatewayStorage,
)
from src.modules.project.infra.external.gateways.gateway_storage_mock import (
    GatewayStorageMock,
)
from src.modules.project.infra.repositories.project_repository_mock import (
    ProjectRepositoryMock,
)
from src.modules.project.infra.repositories.project_repository_neo import (
    ProjectRepositoryNeo,
)
from src.shared.environments.environments import STAGE, env
from src.shared.environments.neo4j_connection_factory import connection

_project_repository = ProjectRepositoryMock()
_gateway_storage = GatewayStorageMock()

def get_gateway_storage():
    if env.stage == 'PROD':
        return GatewayStorage()
    else:
        return _gateway_storage


def get_repo_project() -> IProjectRepository:
    if env.stage == STAGE.PROD:
        return ProjectRepositoryNeo(connection_factory=connection)
    
    return _project_repository
