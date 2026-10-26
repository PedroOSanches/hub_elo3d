from datetime import date
from uuid import UUID

from src.modules.project.domain.entities.project import Project
from src.modules.project.domain.entities.project_file import ProjectFile
from src.modules.project.domain.enums.urgency_enum import Urgency
from src.modules.project.domain.repositories.project_repository_interface import IProjectRepository

class CreateProjectUseCase:
    def __init__(self, repo: IProjectRepository):
        self.repo = repo

    def __call__(
        self,
        title: str,
        date_end: date,
        pieces_quantity: int,
        category: str,
        description: str,
        urgency: Urgency,
        filament_id: UUID,
        files: list[ProjectFile],
        technical_info: str | None = None,
    ) -> Project:
        project = Project(
            title = title,
            date_end = date_end,
            pieces_quantity = pieces_quantity,
            category = category,
            description = description,
            urgency = urgency,
            filament_id = filament_id,
            files = files,
            technical_info = technical_info
        )
        return self.repo.create_project(project = project)