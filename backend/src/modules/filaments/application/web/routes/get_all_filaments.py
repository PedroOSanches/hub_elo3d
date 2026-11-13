from fastapi import APIRouter, Depends, status

from src.modules.filaments.application.controllers.get_all_filaments_controller import (
    GetAllFilamentsController,
)
from src.modules.filaments.application.usecases.get_all_filaments_usecase import (
    GetAllFilamentsUsecase,
)
from src.modules.filaments.application.web.dependencies import get_repo_filament
from src.modules.filaments.application.web.schemas.filament_schema import (
    FilamentResponseSchema,
)

get_all_router = APIRouter()


def get_all_filaments_dependencies() -> GetAllFilamentsController:
    repo = get_repo_filament()
    usecase = GetAllFilamentsUsecase(repo=repo)
    return GetAllFilamentsController(usecase)


@get_all_router.get(
    "/get_all",
    status_code=status.HTTP_200_OK,
    response_model=list[FilamentResponseSchema],
)
async def get_all_filaments(
    controller: GetAllFilamentsController = Depends(get_all_filaments_dependencies),
):
    return controller()