from fastapi import APIRouter, status, Depends
from src.modules.user.application.web.dependencies import get_repo_user
from src.modules.user.application.web.schemas.create_user_schema import CreateUserResponseSchema

from src.modules.user.application.controllers.update_user_controller import UpdateUserController
from src.modules.user.application.usecases.update_user_usecase import UpdateUserUsecase
from src.modules.user.application.web.schemas.update_user_request_schema import UpdateUserRequestSchema
update_user_router = APIRouter()

def get_update_user_dependencies():
    repo = get_repo_user()
    usecase = UpdateUserUsecase(repo)
    return UpdateUserController(usecase)



@update_user_router.post(
        '/update_user', 
        status_code=status.HTTP_200_OK, 
        response_model=CreateUserResponseSchema
        )
async def update_user(
    request: UpdateUserRequestSchema,
    controller: UpdateUserController = Depends(get_update_user_dependencies)
    ):

    return controller(request)