from uuid import UUID

from src.modules.project.application.usecases.get_project_usecase import (
    GetProjectUsecase,
)
from src.modules.project.application.web.schemas.get_project_schema import (
    GetProjectFilesResponseSchema,
    GetProjectResponseSchema,
)
from src.modules.project.domain.gateways.storage_gateway import IGatewayStorage


class GetProjectController:
    def __init__(self, usecase: GetProjectUsecase, gateway_storage: IGatewayStorage):
        self.usecase = usecase
        self.gateway_storage = gateway_storage

    def __call__(self, project_id: UUID) -> GetProjectResponseSchema:
        project = self.usecase(project_id)
        project_data = project.model_dump(mode='python')
        project_data["files"] = [
            GetProjectFilesResponseSchema(
                title = file.title,
                download_url=self.gateway_storage.generate_download_url(
                    file_name=file.title,
                    object_key=file.object_key
                ),
                size=file.size,
                content_type=file.content_type,
            )
            for file in project.files
        ]

        return GetProjectResponseSchema(**project_data)