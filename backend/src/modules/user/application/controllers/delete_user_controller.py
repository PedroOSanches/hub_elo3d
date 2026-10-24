from typing import Any

from uuid import UUID

from src.shared.errors.controller_error import WrongTypeParameter, MissingParameters
from src.modules.user.application.usecases.delete_user_usecase import DeleteUserUsecase
from src.modules.user.application.web.schemas.user_response_schema import UserResponseSchema


class DeleteUserController:

    def __init__(self, usecase: DeleteUserUsecase):
        self.usecase = usecase

    def __call__(self, id: str) -> UserResponseSchema:
        try:
            return UserResponseSchema.model_validate(self.usecase(UUID(id)))

        except ValueError as err:
            raise WrongTypeParameter(
                field_name='id',
                field_type_received=id.__class__.__name__,
                field_type_expected='UUID'
            )