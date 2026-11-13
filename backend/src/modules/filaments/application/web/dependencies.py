from src.modules.filaments.domain.repositories.i_filament_repository import (
    IFilamentRepository,
)
from src.modules.filaments.infra.repositories.filament_repository_mock import (
    FilamentRepositoryMock,
)


_repo_filament = FilamentRepositoryMock()


def get_repo_filament() -> IFilamentRepository:
    return _repo_filament