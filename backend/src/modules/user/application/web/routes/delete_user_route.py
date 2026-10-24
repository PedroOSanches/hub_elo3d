from fastapi import APIRouter, Depends, status


from src.modules.user.application.controllers.delete_user_controller import DeleteUserController
from src.modules.user.application.usecases.delete_user_usecase import DeleteUserUsecase
from src.modules.user.application.web.schemas.user_response_schema import UserResponseSchema
from src.modules.user.application.web.dependencies import get_repo_user

def get_dependencies_delete_user() -> DeleteUserController:
    repo = get_repo_user()
    usecase = DeleteUserUsecase(repo)
    return DeleteUserController(usecase)



delete_user_router = APIRouter()

@delete_user_router.delete('/delete_user/{id}', status_code=status.HTTP_200_OK, response_model=UserResponseSchema)
def delete_user(
    id: str,
    controller: DeleteUserController = Depends(get_dependencies_delete_user)
    ) -> UserResponseSchema:

    return controller(id)