from unittest.mock import Mock
from uuid import uuid7
from pytest import fixture, raises

from src.modules.project.application.usecases.delete_project_usecase import DeleteProjectUsecase
from src.modules.project.domain.entities.project import Project
from src.modules.project.domain.repositories.project_repository_interface import IProjectRepository
from src.modules.project.domain.errors.project_errors import ProjectNotFoundError

@fixture
def repo():
    return Mock(spec=IProjectRepository)

class TestDeleteProjectUsecase:
    def test_delete_existing_project(self, repo):
        project_id = uuid7()
        project = Mock(spec=Project)

        repo.delete_project.return_value = project

        usecase = DeleteProjectUsecase(repo)
        result = usecase(project_id)

        assert result is project
        
        repo.delete_project.assert_called_once_with(project_id)

    def test_delete_nonexistent_project(self, repo):
        project_id = uuid7()

        repo.delete_project.side_effect = ProjectNotFoundError(project_id)
        usecase = DeleteProjectUsecase(repo)

        with raises(
            ProjectNotFoundError,
            match=f"Project {project_id} not found"):
            usecase(project_id)

        repo.delete_project.assert_called_once_with(project_id)