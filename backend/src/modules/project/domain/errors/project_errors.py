from uuid import UUID

from src.shared.errors.usecase_error import NotFoundError

class ProjectNotFoundError(NotFoundError):
    def __init__(self, project_id: UUID):
        super().__init__(f"Project {project_id} not found")