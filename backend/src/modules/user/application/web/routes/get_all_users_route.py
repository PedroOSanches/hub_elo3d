from fastapi import APIRouter, Depends, status

from src.modules.user.application.controllers.get_all_users_controller import GetAllUsersController
from src.modules.user.application.usecases.get_all_users_usecase import GetAllUsersUsecase
from src.modules.user.application.web.dependencies import get_repo_user

def get_dependencies_get_user() -> GetAllUsersController:
    repo = get_repo_user()
    usecase = GetAllUsersUsecase(repo)
    return GetAllUsersController(usecase)


get_all_users_router = APIRouter()


@get_all_users_router.get('/get_all_users', status_code=status.HTTP_200_OK)
def get_all_users(
    controller: GetAllUsersController =  Depends(get_dependencies_get_user)
):

    return controller()