from uuid import uuid4

import pytest

from src.modules.filaments.domain.errors.filament_errors import FilamentNotFoundError
from src.modules.filaments.infra.repositories.filament_repository_mock import (
    FilamentRepositoryMock,
)


class TestFilamentRepositoryMock:
    def setup_method(self):
        self.repo = FilamentRepositoryMock()

    def test_get_all_filaments(self):
        filaments = self.repo.get_all_filaments()

        assert len(filaments) == 4
        assert [f.nome for f in filaments] == ["PLA", "ABS", "PETG", "TPU"]

    def test_get_filament(self):
        existing = self.repo.get_all_filaments()[0]

        assert self.repo.get_filament(existing.id) == existing

    def test_get_filament_not_found(self):
        with pytest.raises(FilamentNotFoundError):
            self.repo.get_filament(uuid4())