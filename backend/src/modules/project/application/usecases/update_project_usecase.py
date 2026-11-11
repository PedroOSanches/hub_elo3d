from typing import Any
from uuid import UUID

from src.modules.project.domain.entities.project import Project
from src.modules.project.domain.repositories.project_repository_interface import IProjectRepository
from src.modules.project.domain.enums.order_status_enum import OrderStatus

class UpdateProjectUsecase:
    EDITABLE_FIELDS = {
        "title",
        "date_end",
        "pieces_quantity",
        "category",
        "description",
        "technical_info",
        "urgency",
        "printer_id",
        "filament_id",
        "files"
    }

    def __init__(self, repo: IProjectRepository):
        self.repo = repo

    def __call__(
            self,
            project_id: UUID,
            changes: dict[str, Any],
            new_status: OrderStatus | None = None
        ) -> Project:
        
        if not changes and new_status is None:
            raise ValueError("Nenhuma alteração foi fornecida")

        invalid_fields = set(changes) - self.EDITABLE_FIELDS

        if invalid_fields:
            raise ValueError(f"Campos inválidos: {', '.join(sorted(invalid_fields))}")

        current_project = self.repo.get_project(project_id)
        project_data = current_project.model_dump(mode="python")
        project_data.update(changes)

        updated_project = Project.model_validate(project_data)

        if new_status is not None:
            updated_project.register_order_status(new_status)

        return self.repo.update_project(project_id, updated_project)