from datetime import date
from uuid import uuid4
from pytest import fixture

from src.modules.project.domain.entities.project import Project
from src.modules.project.domain.entities.project_file import ProjectFile
from src.modules.project.infra.repositories.project_repository_mock import ProjectRepositoryMock

@fixture
def repo():
    return ProjectRepositoryMock()

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

class TestGetAllProjectsRepositoryMock:
    def test_get_all_projects_success(self, repo, valid_project):
        second_project = valid_project.model_copy(update={"id": uuid4(), "title": "Prótese de perna", "category": "prosthesis"})

        repo.create_project(valid_project)
        repo.create_project(second_project)

        response = repo.get_all_projects()

        assert len(response) == 2
        assert valid_project in response
        assert second_project in response

    def test_get_all_projects_empty(self, repo):
        response = repo.get_all_projects()

        assert response == []

    def test_get_all_projects_returns_only_projects_created(self, repo, valid_project):
        repo.create_project(valid_project)

        response = repo.get_all_projects()

        assert len(response) == 1
        assert response[0] is valid_project