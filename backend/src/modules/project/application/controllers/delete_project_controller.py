from typing import Any
from uuid import UUID

from src.modules.project.application.usecases.delete_project_usecase import DeleteProjectUsecase
from src.modules.project.application.web.schemas.get_project_schema import GetProjectResponseSchema

class DeleteProjectController:
    def __init__(self, usecase: DeleteProjectUsecase):
        self.usecase = usecase

    def __call__(self, project_id: UUID) -> dict[str, Any]:
        deleted_project = self.usecase(project_id)

        response = GetProjectResponseSchema.model_validate(deleted_project)

        return response.model_dump(mode="json")