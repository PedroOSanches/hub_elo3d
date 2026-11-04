from datetime import date
from uuid import uuid4
from pytest import raises

from src.modules.project.domain.entities.project import Project
from src.modules.project.domain.entities.project_file import ProjectFile
from src.modules.project.domain.repositories.project_repository_interface import IProjectRepository
from src.modules.project.infra.repositories.project_repository_mock import ProjectRepositoryMock

def valid_project():
    return Project(
        title="Prótese de mão",
        date_end=date(2026, 11, 15),
        pieces_quantity=1,
        category="prosthesis",
        description="Projeto de prótese para reabilitação",
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
    def test_implements_repository_interface(self):
        repo = ProjectRepositoryMock()

        assert isinstance(repo, IProjectRepository)

    def test_create_project(self):
        repo = ProjectRepositoryMock()
        project = valid_project()

        created_project = repo.create_project(project)

        assert created_project == project
        assert repo.projects[project.id] == project
        assert len(repo.projects) == 1

    def test_create_multiple_projects(self):
        repo = ProjectRepositoryMock()
        project1 = valid_project()
        project2 = valid_project()

        repo.create_project(project1)
        repo.create_project(project2)

        assert len(repo.projects) == 2
        assert project1.id in repo.projects
        assert project2.id in repo.projects

    def test_repository_instances_are_independent(self):
        repo1 = ProjectRepositoryMock()
        repo2 = ProjectRepositoryMock()
        repo1.create_project(valid_project())

        assert len(repo1.projects) == 1
        assert len(repo2.projects) == 0

    def test_other_methods_raise_not_implemented_error(self):
        repo = ProjectRepositoryMock()

        with raises(NotImplementedError):
            repo.update_project(uuid4(), valid_project())

        with raises(NotImplementedError):
            repo.delete_project(uuid4())