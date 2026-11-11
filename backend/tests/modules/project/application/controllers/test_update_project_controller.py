import json
from datetime import datetime, date
from uuid import uuid7
from pytest import fixture, raises

from src.modules.project.application.controllers.update_project_controller import UpdateProjectController
from src.modules.project.application.usecases.update_project_usecase import UpdateProjectUsecase
from src.modules.project.application.web.schemas.update_project_schema import UpdateProjectRequestSchema
from src.modules.project.domain.entities.project import Project
from src.modules.project.domain.entities.project_file import ProjectFile
from src.modules.project.domain.enums.order_status_enum import OrderStatus
from src.modules.project.domain.errors.project_errors import ProjectNotFoundError
from src.modules.project.infra.repositories.project_repository_mock import ProjectRepositoryMock

@fixture
def valid_project():
    return Project(
        title="Prótese de mão",
        date_end=date(2026, 11, 15),
        pieces_quantity=1,
        category="prosthesis",
        description="Projeto para reabilitação",
        technical_info="Informação original",
        urgency="high",
        filament_id=uuid7(),
        files=[
            ProjectFile(
                title="Modelo 3D",
                file_url="https://example.com/model.stl"
            )
        ]
    )

@fixture
def repo(valid_project):
    repo = ProjectRepositoryMock()
    repo.create_project(valid_project)
    return repo

@fixture
def controller(repo):
    usecase = UpdateProjectUsecase(repo)
    return UpdateProjectController(usecase)

class TestUpdateProjectController:
    def test_update_only_title(self, controller, repo, valid_project):
        request = UpdateProjectRequestSchema(
            title="Prótese de mão atualizada"
        )

        response = controller(valid_project.id, request)

        assert response["id"] == str(valid_project.id)
        assert response["title"] == "Prótese de mão atualizada"
        assert response["description"] == valid_project.description
        assert repo.get_project(valid_project.id).title == "Prótese de mão atualizada"

        json.dumps(response)

    def test_update_only_status(self, controller, repo, valid_project):
        request = UpdateProjectRequestSchema(
            new_status=OrderStatus.RECEIVED
        )

        response = controller(valid_project.id, request)
        history = response["order_status"]

        assert len(history) == 2
        assert "waiting_for_partner" in history
        assert "received" in history

        timestamps = history["received"]

        assert datetime.fromisoformat(timestamps).tzinfo is not None
        assert OrderStatus.RECEIVED.value in repo.get_project(valid_project.id).order_status

    def test_update_fields_and_status(self, controller, valid_project):
        request = UpdateProjectRequestSchema(
            title="Prótese de mão atualizada",
            new_status=OrderStatus.RECEIVED
        )

        response = controller(valid_project.id, request)

        assert response["title"] == "Prótese de mão atualizada"
        assert "received" in response["order_status"]

    def test_clear_optional_fields(self, controller, repo, valid_project):
        request = UpdateProjectRequestSchema(
            technical_info=None
        )

        response = controller(valid_project.id, request)

        assert response["technical_info"] is None
        assert repo.get_project(valid_project.id).technical_info is None

    def test_nonexistent_project(self, controller):
        project_id = uuid7()
        request = UpdateProjectRequestSchema(
            title="Projeto inexistente"
        )

        with raises(ProjectNotFoundError):
            controller(project_id, request)

    def test_invalid_transition_does_not_save(self, controller, repo, valid_project):
        request = UpdateProjectRequestSchema(
            new_status=OrderStatus.IN_PROGRESS
        )

        original_history = valid_project.order_status.copy()

        with raises(ValueError, match="Status inválido"):
            controller(valid_project.id, request)

        stored_project = repo.get_project(valid_project.id)

        assert stored_project.order_status == original_history