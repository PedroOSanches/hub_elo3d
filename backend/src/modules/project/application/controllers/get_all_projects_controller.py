from typing import Any

from src.modules.project.application.usecases.get_all_projects_usecase import GetAllProjectsUsecase
from src.modules.project.application.web.schemas.get_all_projects_schema import GetAllProjectsResponseSchema

class GetAllProjectsController:
    def __init__(self, usecase: GetAllProjectsUsecase):
        self.usecase = usecase

    def __call__(self) -> list[dict[str, Any]]:
        projects = self.usecase()
        response = GetAllProjectsResponseSchema.model_validate(projects)

        return response.model_dump(mode="json")