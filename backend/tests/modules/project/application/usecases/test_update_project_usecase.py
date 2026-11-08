from datetime import date
from unittest.mock import Mock
from uuid import uuid7
from pytest import fixture, raises
from pydantic import ValidationError

from src.modules.project.application.usecases.update_project_usecase import UpdateProjectUsecase
from src.modules.project.domain.entities.project import Project
from src.modules.project.domain.entities.project_file import ProjectFile
from src.modules.project.domain.enums.order_status_enum import OrderStatus
from src.modules.project.domain.repositories.project_repository_interface import IProjectRepository

@fixture
def valid_project():
    return Project(
        title="Prótese de mão",
        date_end=date(2026, 11, 15),
        pieces_quantity=1,
        category="prosthesis",
        description="Projeto para reabilitação",
        urgency="high",
        filament_id=uuid7(),
        files=[
            ProjectFile(
                title="Modelo 3D",
                file_url="https://example.com/model.stl"
            )
        ],
    )

@fixture
def repo(valid_project):
    repo_mock = Mock(spec=IProjectRepository)
    repo_mock.get_project.return_value = valid_project
    repo_mock.update_project.side_effect = lambda project_id, updated_project: updated_project
    return repo_mock

class TestUpdateProjectUsecase:
    def test_update_project_title(self, repo, valid_project):
        usecase = UpdateProjectUsecase(repo)
        updated = usecase(valid_project.id, {"title": "Nova Prótese de mão"})

        assert updated.title == "Nova Prótese de mão"
        assert updated.description == valid_project.description
        assert updated.id == valid_project.id
        assert valid_project.title == "Prótese de mão"

        repo.update_project.assert_called_once_with(valid_project.id, updated)

    def test_update_preserves_status_history(self, repo, valid_project):
        valid_project.register_order_status(OrderStatus.RECEIVED)
        original_status = valid_project.order_status.copy()
        usecase = UpdateProjectUsecase(repo)
        updated = usecase(valid_project.id, {"description": "Atualização da descrição"})

        assert updated.order_status == original_status
        assert updated.current_order_status == OrderStatus.RECEIVED

    def test_update_with_invalid_data_raises_validation_error(self, repo, valid_project):
        usecase = UpdateProjectUsecase(repo)

        with raises(ValidationError):
            usecase(valid_project.id, {"pieces_quantity": -5})

        repo.update_project.assert_not_called()

    def test_cannot_change_id(self, repo, valid_project):
        usecase = UpdateProjectUsecase(repo)

        with raises(ValueError):
            usecase(valid_project.id, {"id": uuid7()})

        repo.update_project.assert_not_called()

    def test_update_only_status(self, repo, valid_project):
        usecase = UpdateProjectUsecase(repo)
        updated = usecase(valid_project.id, {}, new_status=OrderStatus.RECEIVED)

        assert updated.current_order_status == OrderStatus.RECEIVED
        assert len(updated.order_status) == 2
        assert OrderStatus.WAITING_FOR_PARTNER in updated.order_status
        assert OrderStatus.RECEIVED in updated.order_status

        repo.update_project.assert_called_once_with(valid_project.id, updated)

    def test_update_preserves_existing_status_history(self, repo, valid_project):
        valid_project.register_order_status(OrderStatus.RECEIVED)
        original_status_history = valid_project.order_status.copy()
        usecase = UpdateProjectUsecase(repo)
        updated = usecase(valid_project.id, {"title": "Prótese atualizada"}, new_status=OrderStatus.IN_PROGRESS)

        for status, timestamp in original_status_history.items():
            assert updated.order_status[status] == timestamp

        assert OrderStatus.IN_PROGRESS in updated.order_status
        assert updated.current_order_status == OrderStatus.IN_PROGRESS
        assert updated.title == "Prótese atualizada"
        assert OrderStatus.IN_PROGRESS not in valid_project.order_status

    def test_duplicate_status_registration_raises_error(self, repo, valid_project):
        usecase = UpdateProjectUsecase(repo)

        with raises(ValueError, match="Status já registrado"):
            usecase(valid_project.id, {}, new_status=OrderStatus.WAITING_FOR_PARTNER)

        repo.update_project.assert_not_called()

    def test_empty_update_does_not_save(self, repo, valid_project):
        usecase = UpdateProjectUsecase(repo)

        with raises(ValueError, match="Nenhuma alteração foi fornecida"):
            usecase(valid_project.id, {})

        repo.update_project.assert_not_called()

    def test_cannot_replace_status_history(self, repo, valid_project):
        usecase = UpdateProjectUsecase(repo)

        with raises(ValueError, match="Campos inválidos"):
            usecase(valid_project.id, {"order_status": {}})

        repo.update_project.assert_not_called()

    def test_invalid_status_transition_raises_error(self, repo, valid_project):
        usecase = UpdateProjectUsecase(repo)

        with raises(ValueError, match="Status inválido"):
            usecase(valid_project.id, {}, new_status=OrderStatus.IN_PROGRESS)

        repo.update_project.assert_not_called()

        assert valid_project.current_order_status == OrderStatus.WAITING_FOR_PARTNER