from uuid import uuid7

from src.modules.storage.application.web.schemas.generate_upload_urls_request import (
    UploadFileRequest,
)
from src.modules.storage.application.web.schemas.upload_urls_response import (
    UploadUrlResponseSchema,
)
from src.modules.storage.domain.gateways.gateway_storage_interface import (
    IGatewayStorage,
)


class UploadUrlUsecase:

    def __init__(self, gateway: IGatewayStorage) -> None:
        self.gateway = gateway

    def __call__(
            self,
            files: list[UploadFileRequest]
            ) -> list[UploadUrlResponseSchema]:

        urls_generated: list[UploadUrlResponseSchema]  = []
        
        for file in files:
            object_key = str(uuid7())
            url = self.gateway.generate_upload_url(
                object_key=object_key,
                content_type=file.content_type
                )
            urls_generated.append(
                UploadUrlResponseSchema(
                    object_key=object_key,
                    upload_url=url
                )
            )

        return urls_generated