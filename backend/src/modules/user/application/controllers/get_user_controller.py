from src.modules.user.application.web.schemas.get_user_schema import GetUserRequestSchema
from src.modules.user.application.usecases.get_user_usecase import GetUserUsecase
from src.modules.user.application.web.schemas.user_response_schema import UserResponseSchema


class GetUserController:
    def __init__(self, usecase: GetUserUsecase) -> None:
        self.usecase = usecase


    def __call__(self, request: GetUserRequestSchema) -> dict:
        user = self.usecase(
            id=request.id
            )

        return UserResponseSchema.model_validate(user).model_dump(mode='json')