from src.modules.filaments.domain.entities.filament import Filament
from src.modules.filaments.domain.repositories.i_filament_repository import (
    IFilamentRepository,
)


class GetAllFilamentsUsecase:

    def __init__(self, repo: IFilamentRepository):
        self.repo = repo

    def __call__(self) -> list[Filament]:
        return self.repo.get_all_filaments()