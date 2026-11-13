from uuid import uuid4

import pytest

from src.modules.filaments.application.usecases.get_all_filaments_usecase import (
    GetAllFilamentsUsecase,
)
from src.modules.filaments.application.usecases.get_filament_usecase import (
    GetFilamentUsecase,
)
from src.modules.filaments.domain.errors.filament_errors import FilamentNotFoundError
from src.modules.filaments.infra.repositories.filament_repository_mock import (
    FilamentRepositoryMock,
)


class TestGetFilamentUsecase:
    def test_get_filament(self):
        repo = FilamentRepositoryMock()
        existing = repo.get_all_filaments()[1]

        assert GetFilamentUsecase(repo)(existing.id) == existing

    def test_get_filament_not_found(self):
        with pytest.raises(FilamentNotFoundError):
            GetFilamentUsecase(FilamentRepositoryMock())(uuid4())


class TestGetAllFilamentsUsecase:
    def test_get_all_filaments(self):
        repo = FilamentRepositoryMock()

        assert GetAllFilamentsUsecase(repo)() == repo.get_all_filaments()