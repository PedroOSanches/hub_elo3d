from fastapi import APIRouter, Depends

from src.modules.storage.application.controllers.generate_upload_url_controller import (
    UploadUrlController,
)
from src.modules.storage.application.usecases.generate_upload_url_usecase import (
    UploadUrlUsecase,
)
from src.modules.storage.application.web.schemas.generate_upload_urls_request import (
    GenerateUrlRequestSchema,
)
from src.modules.storage.application.web.schemas.upload_urls_response import (
    UploadUrlResponseSchema,
)

from ..dependencies import get_gateway_s3


def get_dependencies_upload_url():
    
    gateway = get_gateway_s3()
    usecase = UploadUrlUsecase(gateway)
    return UploadUrlController(usecase)

generate_upload_route = APIRouter()

@generate_upload_route.post(
        path='/generate_upload_url', 
        response_model=list[UploadUrlResponseSchema]
        )
def generate_upload_url(
    request: GenerateUrlRequestSchema,
    controller: UploadUrlController = Depends(get_dependencies_upload_url)
    ) -> list[UploadUrlResponseSchema]:

    return controller(request)