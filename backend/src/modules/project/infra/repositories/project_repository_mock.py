
from datetime import date
from uuid import UUID

from src.modules.project.domain.entities.project import Project
from src.modules.project.domain.entities.project_file import ProjectFile
from src.modules.project.domain.enums.category_enum import Category
from src.modules.project.domain.enums.urgency_enum import Urgency
from src.modules.project.domain.errors.project_errors import ProjectNotFoundError
from src.modules.project.domain.repositories.project_repository_interface import (
    IProjectRepository,
)


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
    
    def available_projects(self, user_id: UUID) -> list[Project]:
        return [
            Project(
                title='Teste',
                date_end=date(2026, 12, 24),
                pieces_quantity=1,
                category=Category('prosthesis'),
                description='Teste',
                urgency=Urgency('low'),
                filament_id=UUID('01a2147b-0a56-773c-9462-412976ac7b86'),
                files=[
                    ProjectFile(
                        title='test.txt',
                        object_key='projects/teste/test.txt',
                        size=1000,
                        content_type='text/plain'
                    )
                ]
            )
        ]