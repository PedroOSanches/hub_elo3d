from uuid import UUID

from src.modules.project.domain.entities.project import Project
from src.modules.project.domain.repositories.project_repository_interface import IProjectRepository
from src.modules.project.domain.enums.order_status_enum import OrderStatus
from src.modules.project.domain.errors.project_errors import ProjectDeletionConflictError

class DeleteProjectUsecase:
    def __init__(self, repo: IProjectRepository):
        self.repo = repo

    def __call__(self, project_id: UUID) -> Project:
        project = self.repo.get_project(project_id)

        if project.current_order_status != OrderStatus.WAITING_FOR_PARTNER:
            raise ProjectDeletionConflictError("O projeto só pode ser excluído enquanto estiver aguardando parceiro")

        return self.repo.delete_project(project_id)