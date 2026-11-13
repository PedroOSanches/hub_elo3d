from uuid import UUID

from src.shared.errors.usecase_error import NotFoundError


class FilamentNotFoundError(NotFoundError):
    def __init__(self, filament_id: UUID) -> None:
        super().__init__(f"Filament {filament_id} not found")