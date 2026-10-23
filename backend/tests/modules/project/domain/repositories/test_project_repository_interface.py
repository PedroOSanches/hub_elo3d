from inspect import isabstract
from pytest import raises

from src.modules.project.domain.repositories.project_repository_interface import IProjectRepository

class TestProjectRepositoryInterface:

    def test_repository_is_abstract(self):
        assert isabstract(IProjectRepository)

    def test_repository_cannot_be_instantiated(self):
        with raises(TypeError):
            IProjectRepository()

    def test_repository_has_required_methods(self):
        expected_methods = {
            "get_project",
            "get_all_projects",
            "create_project",
            "update_project",
            "delete_project"
        }
        
        assert expected_methods == IProjectRepository.__abstractmethods__