from abc import ABC, abstractmethod
from uuid import UUID

from src.modules.project.domain.entities.project import Project

class IProjectRepository(ABC):
    @abstractmethod
    def get_project(self, project_id: UUID) -> Project:
        pass

    @abstractmethod
    def get_all_projects(self) -> list[Project]:
        pass

    @abstractmethod
    def create_project(self, project: Project) -> Project:
        pass

    @abstractmethod
    def update_project(
        self,
        project_id: UUID,
        updated_project: Project
    ) -> Project:
        pass

    @abstractmethod
    def delete_project(self, project_id: UUID) -> Project:
        pass