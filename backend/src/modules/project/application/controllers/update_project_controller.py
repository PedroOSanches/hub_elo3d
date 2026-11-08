from typing import Any
from uuid import UUID

from src.modules.project.application.usecases.update_project_usecase import UpdateProjectUsecase
from src.modules.project.application.web.schemas.update_project_schema import UpdateProjectRequestSchema, UpdateProjectResponseSchema

class UpdateProjectController:
    def __init__(self, usecase: UpdateProjectUsecase):
        self.usecase = usecase

    def __call__(self, project_id: UUID, request: UpdateProjectRequestSchema) -> dict[str, Any]:
        changes = request.model_dump(exclude_unset=True, exclude={"new_status"})

        updated_project = self.usecase(project_id, changes=changes, new_status=request.new_status)

        response = UpdateProjectResponseSchema.model_validate(updated_project)

        return response.model_dump(mode="json")