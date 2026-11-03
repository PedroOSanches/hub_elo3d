from datetime import date
from uuid import uuid4
from pytest import fixture, raises

from src.modules.project.domain.entities.project import Project
from src.modules.project.domain.entities.project_file import ProjectFile
from src.modules.project.infra.repositories.project_repository_mock import ProjectRepositoryMock

@fixture
def repo():
    return ProjectRepositoryMock()

@fixture
def valid_project():
    return Project(
        id=uuid4(),
        title="Prótese de mão",
        date_end=date(2026, 11, 15),
        pieces_quantity=1,
        category="Ortopedia",
        description="Projeto de prótese para reabilitação",
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

class TestProjectRepositoryMock:
    def test_get_project_success(self, repo, valid_project):
        repo.create_project(valid_project)

        response = repo.get_project(valid_project.id)

        assert response is valid_project

    def test_get_project_not_found(self, repo):
        with raises(Exception) as exc_info:
            repo.get_project(uuid4())

        assert str(exc_info.value) == "Project not found"

    def test_get_correct_project(self, repo, valid_project):
        other_project = valid_project.model_copy(update={"id": uuid4(), "title": "Outro projeto"})

        repo.create_project(valid_project)
        repo.create_project(other_project)

        response = repo.get_project(other_project.id)

        assert response.id == other_project.id
        assert response.title == "Outro projeto"
        assert response.id != valid_project.id