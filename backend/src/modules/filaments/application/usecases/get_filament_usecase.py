from uuid import UUID

from src.modules.filaments.domain.entities.filament import Filament
from src.modules.filaments.domain.repositories.i_filament_repository import (
    IFilamentRepository,
)


class GetFilamentUsecase:

    def __init__(self, repo: IFilamentRepository):
        self.repo = repo

    def __call__(self, filament_id: UUID) -> Filament:
        return self.repo.get_filament(filament_id)