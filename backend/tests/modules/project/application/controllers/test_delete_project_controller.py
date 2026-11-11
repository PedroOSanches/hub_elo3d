from datetime import date, datetime
from uuid import uuid7
from unittest.mock import Mock
from pytest import fixture, raises

from src.modules.project.application.controllers.delete_project_controller import DeleteProjectController
from src.modules.project.application.usecases.delete_project_usecase import DeleteProjectUsecase
from src.modules.project.domain.entities.project import Project
from src.modules.project.domain.entities.project_file import ProjectFile
from src.modules.project.domain.repositories.project_repository_interface import IProjectRepository
from src.modules.project.domain.errors.project_errors import ProjectNotFoundError

@fixture
def repo():
    return Mock(spec=IProjectRepository)

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
        ]
    )

class TestDeleteProjectController:
    def test_delete_existing_project(self, repo, valid_project):
        repo.delete_project.return_value = valid_project

        usecase = DeleteProjectUsecase(repo)
        controller = DeleteProjectController(usecase)

        repo.get_project.return_value = valid_project

        response = controller(valid_project.id)

        assert response["id"] == str(valid_project.id)
        assert response["title"] == valid_project.title
        assert response["pieces_quantity"] == 1

        repo.delete_project.assert_called_once_with(valid_project.id)

    def test_controller_serializes_deleted_project(self, repo, valid_project):
        repo.delete_project.return_value = valid_project

        usecase = DeleteProjectUsecase(repo)
        controller = DeleteProjectController(usecase)

        repo.get_project.return_value = valid_project

        response = controller(valid_project.id)

        assert response["date_end"] == "2026-11-15"
        assert response["filament_id"] == str(valid_project.filament_id)
        assert response["urgency"] == "high"
        assert response["files"][0]["title"] == "Modelo 3D"
        assert "waiting_for_partner" in response["order_status"]

        timestamp = response["order_status"]["waiting_for_partner"]

        assert datetime.fromisoformat(timestamp).tzinfo is not None

    def test_delete_nonexistent_project(self, repo):
        project_id = uuid7()

        repo.get_project.side_effect = ProjectNotFoundError(project_id)

        usecase = DeleteProjectUsecase(repo)
        controller = DeleteProjectController(usecase)

        with raises(ProjectNotFoundError, match=f"Project {project_id} not found"):
            controller(project_id)

        repo.delete_project.assert_not_called()