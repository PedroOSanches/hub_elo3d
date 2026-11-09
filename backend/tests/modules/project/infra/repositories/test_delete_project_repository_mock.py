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
        ]
    )

class TestDeleteProjectRepositoryMock:

    def test_delete_existing_project(self, repo, valid_project):
        repo.create_project(valid_project)

        deleted_project = repo.delete_project(valid_project.id)

        assert deleted_project == valid_project
        assert valid_project.id not in repo.projects

        with raises(ProjectNotFoundError):
            repo.get_project(valid_project.id)

    def test_delete_nonexistent_project(self, repo):
        with raises(ProjectNotFoundError):
            repo.delete_project(uuid7())

    def test_delete_preserves_other_projects(self, repo, valid_project):
        other_project = valid_project.model_copy(
            update={
                "id": uuid7(),
                "title": "Prótese de perna"
            }
        )

        repo.create_project(valid_project)
        repo.create_project(other_project)

        repo.delete_project(valid_project.id)

        assert len(repo.projects) == 1
        assert repo.get_project(other_project.id) == other_project