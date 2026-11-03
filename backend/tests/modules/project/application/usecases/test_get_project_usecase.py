from unittest.mock import Mock
from uuid import uuid4
from pytest import fixture, raises

from src.modules.project.application.usecases.get_project_usecase import GetProjectUsecase
from src.modules.project.domain.entities.project import Project
from src.modules.project.domain.repositories.project_repository_interface import IProjectRepository

@fixture
def repo():
    return Mock(spec=IProjectRepository)

class TestGetProjectUsecase:
    def test_get_existing_project(self, repo):
        project_id = uuid4()
        project = Mock(spec=Project)
        repo.get_project.return_value = project

        usecase = GetProjectUsecase(repo)
        result = usecase(project_id)

        assert result is project
        repo.get_project.assert_called_once_with(project_id)

    def test_get_non_existing_project(self, repo):
        project_id = uuid4()
        repo.get_project.side_effect = Exception("Project not found")

        usecase = GetProjectUsecase(repo)

        with raises(Exception) as exc_info:
            usecase(project_id)

        assert str(exc_info.value) == "Project not found"
        repo.get_project.assert_called_once_with(project_id)