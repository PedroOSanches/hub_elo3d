from datetime import date
from uuid import uuid4
from unittest.mock import Mock
from pytest import fixture, raises

from src.modules.project.application.controllers.get_project_controller import GetProjectController
from src.modules.project.application.usecases.get_project_usecase import GetProjectUsecase
from src.modules.project.domain.entities.project import Project
from src.modules.project.domain.entities.project_file import ProjectFile
from src.modules.project.domain.repositories.project_repository_interface import IProjectRepository

@fixture
def repo():
    return Mock(spec=IProjectRepository)

@fixture
def valid_project():
    return Project(
        id=uuid4(),
        title="Prótese de mão",
        date_end=date(2026, 11, 15),
        pieces_quantity=1,
        category="Ortopedia",
        description="Projeto para reabilitação",
        technical_info=None,
        urgency="high",
        filament_id=uuid4(),
        files=[
            ProjectFile(
                title="Modelo 3D",
                file_url="https://example.com/model.stl"
            )
        ]
    )

class TestGetProjectController:
    def test_get_project_controller(self, repo, valid_project):
        repo.get_project.return_value = valid_project
        usecase = GetProjectUsecase(repo)
        controller = GetProjectController(usecase)

        response = controller(valid_project.id)

        assert response["id"] == str(valid_project.id)
        assert response["title"] == valid_project.title
        assert response["pieces_quantity"] == 1
        assert response["order_status"] == "waiting_for_partner"

        repo.get_project.assert_called_once_with(valid_project.id)

    def test_controller_serializes_project(self, repo, valid_project):
        repo.get_project.return_value = valid_project
        usecase = GetProjectUsecase(repo)
        controller = GetProjectController(usecase)

        response = controller(valid_project.id)

        assert response["date_end"] == "2026-11-15"
        assert response["filament_id"] == str(valid_project.filament_id)
        assert response["urgency"] == "high"
        assert response["files"][0]["title"] == "Modelo 3D"

    def test_controller_with_nonexistent_project(self, repo):
        project_id = uuid4()
        repo.get_project.side_effect = Exception("Project not found")
        usecase = GetProjectUsecase(repo)
        controller = GetProjectController(usecase)

        with raises(Exception, match="Project not found"):
            controller(project_id)

        repo.get_project.assert_called_once_with(project_id)