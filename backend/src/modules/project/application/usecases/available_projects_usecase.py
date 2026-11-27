from typing import Any
from uuid import UUID

from src.modules.project.domain.repositories.project_repository_interface import (
    IProjectRepository,
)


class AvailableProjectsUsecase:

    def __init__(self, repo: IProjectRepository) -> None:
        self.repo = repo

    def __call__(self, user_id: UUID) -> Any:
        return self.repo.available_projects(user_id=user_id)