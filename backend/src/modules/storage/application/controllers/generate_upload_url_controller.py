
from src.modules.storage.application.usecases.generate_upload_url_usecase import (
    UploadUrlUsecase,
)
from src.modules.storage.application.web.schemas.generate_upload_urls_request import (
    GenerateUrlRequestSchema,
)
from src.modules.storage.application.web.schemas.upload_urls_response import (
    UploadUrlResponseSchema,
)


class UploadUrlController:

    def __init__(self, usecase: UploadUrlUsecase) -> None:
        self.usecase = usecase

    def __call__(
            self, 
            request: GenerateUrlRequestSchema
            ) -> list[UploadUrlResponseSchema]:

        return self.usecase(
            files=request.files
        )