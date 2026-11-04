from datetime import date
from unittest.mock import Mock
from uuid import uuid4
from pytest import fixture

from src.modules.project.application.controllers.get_all_projects_controller import GetAllProjectsController
from src.modules.project.application.usecases.get_all_projects_usecase import GetAllProjectsUsecase
from src.modules.project.domain.entities.project import Project
from src.modules.project.domain.entities.project_file import ProjectFile
from src.modules.project.domain.repositories.project_repository_interface import IProjectRepository

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
        filament_id=uuid4(),
        files=[
            ProjectFile(
                title="Modelo 3D",
                file_url="https://example.com/model.stl",
            )
        ],
    )

class TestGetAllProjectsController:
    def test_get_all_projects_success(self, repo, valid_project):
        second_project = valid_project.model_copy(update={"id": uuid4(), "title": "Prótese de perna", "category": "prosthesis"})

        repo.get_all_projects.return_value = [valid_project, second_project]

        usecase = GetAllProjectsUsecase(repo)
        controller = GetAllProjectsController(usecase)
        response = controller()

        assert len(response) == 2
        assert response[0]["id"] == str(valid_project.id)
        assert response[1]["title"] == "Prótese de perna"
        assert response[1]["category"] == "prosthesis"

        repo.get_all_projects.assert_called_once_with()

    def test_get_all_projects_empty(self, repo):
        repo.get_all_projects.return_value = []

        usecase = GetAllProjectsUsecase(repo)
        controller = GetAllProjectsController(usecase)
        response = controller()

        assert response == []

        repo.get_all_projects.assert_called_once_with()

    def test_controller_serializes_projects(self, repo, valid_project):
        repo.get_all_projects.return_value = [valid_project]

        usecase = GetAllProjectsUsecase(repo)
        controller = GetAllProjectsController(usecase)
        response = controller()

        assert isinstance(response, list)
        assert response[0]["date_end"] == "2026-11-15"
        assert response[0]["urgency"] == "high"
        assert response[0]["order_status"] == "waiting_for_partner"
        assert response[0]["files"][0]["title"] == "Modelo 3D"