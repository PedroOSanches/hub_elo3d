from uuid import UUID

from src.shared.errors.usecase_error import NotFoundError


class ProjectNotFoundError(NotFoundError):
    def __init__(self, project_id: UUID):
        super().__init__(f"Project {project_id} not found")

class NoProjectsAvailable(NotFoundError):
    def __init__(self):
        super().__init__("No projects available for recommendation.")

class ProjectStatusConflictError(ValueError):
    pass

class ProjectDeletionConflictError(ValueError):
    pass