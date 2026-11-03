from uuid import UUID
from typing import Any

from src.modules.project.application.usecases.get_project_usecase import GetProjectUsecase
from src.modules.project.application.web.schemas.get_project_schema import GetProjectResponseSchema

class GetProjectController:
    def __init__(self, usecase: GetProjectUsecase):
        self.usecase = usecase

    def __call__(self, project_id: UUID) -> dict[str, Any]:
        project = self.usecase(project_id)
        response = GetProjectResponseSchema.model_validate(project)

        return response.model_dump(mode="json")