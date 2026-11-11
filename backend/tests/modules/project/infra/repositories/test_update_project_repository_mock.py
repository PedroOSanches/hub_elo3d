from datetime import date
from uuid import uuid7
from pytest import fixture, raises

from src.modules.project.domain.entities.project import Project
from src.modules.project.domain.entities.project_file import ProjectFile
from src.modules.project.domain.errors.project_errors import ProjectNotFoundError
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
        filament_id=uuid7(),
        files=[
            ProjectFile(
                title="Modelo 3D",
                file_url="https://example.com/model.stl"
            )
        ],
    )

class TestUpdateProjectRepositoryMock:
    def test_update_existing_project(self, repo, valid_project):
        repo.create_project(valid_project)

        updated_project = valid_project.model_copy(update={"title": "Prótese de mão Atualizada"})

        result = repo.update_project(valid_project.id, updated_project)

        assert result.title == "Prótese de mão Atualizada"
        assert result.id == valid_project.id
        assert repo.get_project(valid_project.id) is updated_project
        assert len(repo.projects) == 1

    def test_update_non_existing_project(self, repo, valid_project):
        nonexistent_id = uuid7()

        with raises(ProjectNotFoundError):
            repo.update_project(nonexistent_id, valid_project)

    def test_update_cannot_change_id(self, repo, valid_project):
        repo.create_project(valid_project)

        updated_project = valid_project.model_copy(update={"id": uuid7()})

        with raises(ValueError):
            repo.update_project(valid_project.id, updated_project)

        assert repo.get_project(valid_project.id) is valid_project
        assert len(repo.projects) == 1