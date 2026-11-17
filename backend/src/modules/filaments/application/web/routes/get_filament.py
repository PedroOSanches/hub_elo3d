from fastapi import APIRouter, Depends, status

from src.modules.filaments.application.controllers.get_filament_controller import (
    GetFilamentController,
)
from src.modules.filaments.application.usecases.get_filament_usecase import (
    GetFilamentUsecase,
)
from src.modules.filaments.application.web.dependencies import get_repo_filament
from src.modules.filaments.application.web.schemas.filament_schema import (
    FilamentResponseSchema,
)
from src.modules.filaments.application.web.schemas.get_filament_schema import (
    GetFilamentRequestSchema,
)

get_router = APIRouter()


def get_filament_dependencies() -> GetFilamentController:
    repo = get_repo_filament()
    usecase = GetFilamentUsecase(repo=repo)
    return GetFilamentController(usecase)


@get_router.get(
    "/get/{filament_id}",
    status_code=status.HTTP_200_OK,
    response_model=FilamentResponseSchema,
)
async def get_filament(
    filament_id: str,
    controller: GetFilamentController = Depends(get_filament_dependencies),
):
    request = GetFilamentRequestSchema(filament_id=filament_id)  # type: ignore
    return controller(request)