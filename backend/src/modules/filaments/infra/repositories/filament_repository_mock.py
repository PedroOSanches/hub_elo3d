from uuid import UUID

from src.modules.filaments.domain.entities.filament import Filament
from src.modules.filaments.domain.errors.filament_errors import FilamentNotFoundError
from src.modules.filaments.domain.repositories.i_filament_repository import (
    IFilamentRepository,
)


class FilamentRepositoryMock(IFilamentRepository):
    """Repositório em memória, com filamentos de exemplo (ids fixos)."""

    def __init__(self) -> None:
        self.filaments: dict[UUID, Filament] = {
            f.id: f
            for f in [
                Filament(
                    id=UUID("9f1c2a10-6b1e-4d3a-8c55-0a1b2c3d4e01"),
                    nome="PLA",
                    tipo="PLA",
                ),
                Filament(
                    id=UUID("9f1c2a10-6b1e-4d3a-8c55-0a1b2c3d4e02"),
                    nome="ABS",
                    tipo="ABS",
                ),
                Filament(
                    id=UUID("9f1c2a10-6b1e-4d3a-8c55-0a1b2c3d4e03"),
                    nome="PETG",
                    tipo="PETG",
                ),
                Filament(
                    id=UUID("9f1c2a10-6b1e-4d3a-8c55-0a1b2c3d4e04"),
                    nome="TPU",
                    tipo="TPU",
                ),
            ]
        }

    def get_filament(self, filament_id: UUID) -> Filament:
        filament = self.filaments.get(filament_id)
        if filament is None:
            raise FilamentNotFoundError(filament_id)
        return filament

    def get_all_filaments(self) -> list[Filament]:
        return list(self.filaments.values())