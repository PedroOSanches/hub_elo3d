
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
        return list(self.projects.values())

    def update_project(
        self,
        project_id: UUID,
        updated_project: Project
    ) -> Project:
        if project_id not in self.projects:
            raise ProjectNotFoundError(project_id)

        if updated_project.id != project_id:
            raise ValueError("Project ID cannot be changed")

        self.projects[project_id] = updated_project

        return updated_project

    def delete_project(self, project_id: UUID) -> Project:
        if project_id not in self.projects:
            raise ProjectNotFoundError(project_id)

        deleted_project = self.projects.pop(project_id)

        return deleted_project