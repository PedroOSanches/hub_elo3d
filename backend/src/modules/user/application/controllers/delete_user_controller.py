from typing import Any

from uuid import UUID

from src.modules.user.application.web.schemas.delete_user_schema import DeleteUserRequestSchema
from src.shared.errors.controller_error import WrongTypeParameter, MissingParameters
from src.modules.user.application.usecases.delete_user_usecase import DeleteUserUsecase
from src.modules.user.application.web.schemas.user_response_schema import UserResponseSchema


class DeleteUserController:

    def __init__(self, usecase: DeleteUserUsecase):
        self.usecase = usecase

    def __call__(self, request: DeleteUserRequestSchema) -> UserResponseSchema:
        
            return UserResponseSchema.model_validate(self.usecase(request.id))