from src.modules.filaments.application.usecases.get_all_filaments_usecase import (
    GetAllFilamentsUsecase,
)
from src.modules.filaments.application.web.schemas.filament_schema import (
    FilamentResponseSchema,
)


class GetAllFilamentsController:

    def __init__(self, usecase: GetAllFilamentsUsecase) -> None:
        self.usecase = usecase

    def __call__(self) -> list[FilamentResponseSchema]:
        return [
            FilamentResponseSchema.model_validate(filament)
            for filament in self.usecase()
        ]