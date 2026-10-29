from src.modules.user.application.usecases.get_all_users_usecase import GetAllUsersUsecase
from src.modules.user.application.web.schemas.user_response_schema import UserResponseSchema

class GetAllUsersController:

    def __init__(self, usecase: GetAllUsersUsecase) -> None:
        self.usecase = usecase

    def __call__(self) -> list[dict]:
        return [UserResponseSchema.model_validate(user).model_dump(mode='json') for user in self.usecase()]