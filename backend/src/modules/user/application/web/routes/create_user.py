from fastapi import APIRouter, status, Depends

from src.modules.user.application.web.schemas.create_user_schema import CreateUserRequestSchema
from src.modules.user.application.web.dependencies import get_repo_user
from src.modules.user.application.controllers.create_user_controller import CreateUserController
from src.modules.user.application.usecases.create_user_usecase import CreateUserUsecase

create_router = APIRouter()

    
def get_create_user_dependecies() -> CreateUserController:
    repo = get_repo_user()
    usecase = CreateUserUsecase(repo)
    controller = CreateUserController(usecase)
    return controller


@create_router.post("/create")
def create_user(
    request: CreateUserRequestSchema,
    controller: CreateUserController = Depends(get_create_user_dependecies),
):
    
    return controller(request)
        