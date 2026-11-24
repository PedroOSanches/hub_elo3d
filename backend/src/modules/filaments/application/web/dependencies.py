from src.modules.filaments.domain.repositories.i_filament_repository import (
    IFilamentRepository,
)
from src.modules.filaments.infra.repositories import (
    FilamentRepositoryMock,
    FilamentRepositoryNeo,
)
from src.shared.environments.environments import env
from src.shared.environments.neo4j_connection_factory import connection

_repo_filament = FilamentRepositoryMock()


def get_repo_filament() -> IFilamentRepository:
    if env.stage.value == 'PROD':
        return FilamentRepositoryNeo(connection=connection)
    return _repo_filament