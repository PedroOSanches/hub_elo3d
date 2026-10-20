from fastapi import APIRouter, status, Depends

from src.modules.user.application.web.dependencies import get_repo_user

from src.modules.user.application.web.schemas.get_user_schema import GetUserRequestSchema
from src.modules.user.application.controllers.get_user_controller import GetUserController
from src.modules.user.application.usecases.get_user_usecase import GetUserUsecase


get_user_router = APIRouter()


def get_dependencies_get_user() -> GetUserController:
    repo = get_repo_user()
    usecase = GetUserUsecase(repo)
    return GetUserController(usecase)

@get_user_router.get('/get_user', status_code=status.HTTP_200_OK)
async def get_user(
    request: GetUserRequestSchema,
    controller: GetUserController = Depends(get_dependencies_get_user)
):
    return controller(request)