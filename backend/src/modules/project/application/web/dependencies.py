from src.modules.project.domain.repositories.project_repository_interface import IProjectRepository
from src.modules.project.infra.repositories.project_repository_mock import ProjectRepositoryMock

_project_repository = ProjectRepositoryMock()

def get_repo_project() -> IProjectRepository:
    return _project_repository