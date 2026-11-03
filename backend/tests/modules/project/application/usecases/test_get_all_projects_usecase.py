from unittest.mock import Mock
from pytest import fixture

from src.modules.project.application.usecases.get_all_projects_usecase import GetAllProjectsUsecase
from src.modules.project.domain.entities.project import Project
from src.modules.project.domain.repositories.project_repository_interface import IProjectRepository

@fixture
def repo():
    return Mock(spec=IProjectRepository)

class TestGetAllProjectsUsecase:
    def test_get_all_projects_success(self, repo):
        projects = [
            Mock(spec=Project),
            Mock(spec=Project)
        ]

        repo.get_all_projects.return_value = projects
        usecase = GetAllProjectsUsecase(repo)
        response = usecase()

        assert response is projects
        assert len(response) == 2

        repo.get_all_projects.assert_called_once_with()

    def test_get_all_projects_empty(self, repo):
        repo.get_all_projects.return_value = []

        usecase = GetAllProjectsUsecase(repo)
        response = usecase()

        assert response == []
        
        repo.get_all_projects.assert_called_once_with()