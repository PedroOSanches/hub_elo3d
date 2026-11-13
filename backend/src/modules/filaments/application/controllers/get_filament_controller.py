from src.modules.filaments.application.usecases.get_filament_usecase import (
    GetFilamentUsecase,
)
from src.modules.filaments.application.web.schemas.filament_schema import (
    FilamentResponseSchema,
)
from src.modules.filaments.application.web.schemas.get_filament_schema import (
    GetFilamentRequestSchema,
)


class GetFilamentController:

    def __init__(self, usecase: GetFilamentUsecase) -> None:
        self.usecase = usecase

    def __call__(self, request: GetFilamentRequestSchema) -> FilamentResponseSchema:
        filament = self.usecase(request.filament_id)
        return FilamentResponseSchema.model_validate(filament)