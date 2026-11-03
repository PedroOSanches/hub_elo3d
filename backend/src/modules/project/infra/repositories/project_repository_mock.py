
from uuid import UUID

from src.modules.project.domain.entities.project import Project
from src.modules.project.domain.repositories.project_repository_interface import IProjectRepository
from src.modules.project.domain.errors.project_errors import ProjectNotFoundError


class ProjectRepositoryMock(IProjectRepository):

    def __init__(self):
        self.projects: dict[UUID, Project] = {}

    def create_project(self, project: Project) -> Project:
        self.projects[project.id] = project
        return project

    def get_project(self, project_id: UUID) -> Project:
        project = self.projects.get(project_id)

        if project is None:
            raise ProjectNotFoundError(project_id)

        return project

    def get_all_projects(self) -> list[Project]:
        raise NotImplementedError

    def update_project(
        self,
        project_id: UUID,
        update_project: Project
    ) -> Project:
        raise NotImplementedError

    def delete_project(self, project_id: UUID) -> Project:
        raise NotImplementedError
