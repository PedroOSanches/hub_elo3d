from src.modules.user.application.web.schemas.create_user_schema import CreateUserRequestSchema
from src.modules.user.application.web.schemas.user_response_schema import UserResponseSchema
from src.modules.user.application.usecases.create_user_usecase import CreateUserUsecase

class CreateUserController :

    def __init__(self, usecase: CreateUserUsecase):
        self.usecase = usecase

    def __call__(self, request: CreateUserRequestSchema) -> UserResponseSchema:
        user = self.usecase(
            name=request.name,
            email=request.email,
            phone=request.phone,
            address=request.address,
            role=request.role,
            password=request.password
        )

        return UserResponseSchema.model_validate(user)
