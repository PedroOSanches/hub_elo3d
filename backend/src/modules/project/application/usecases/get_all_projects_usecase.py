from src.modules.project.domain.entities.project import Project
from src.modules.project.domain.repositories.project_repository_interface import IProjectRepository

class GetAllProjectsUsecase:
    def __init__(self, repo: IProjectRepository):
        self.repo = repo

    def __call__(self,) -> list[Project]:
        return self.repo.get_all_projects()