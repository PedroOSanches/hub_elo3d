from typing import Any

from src.modules.user.domain.repositories.user_repository_interface import IUserRepository
from src.modules.user.application.usecases.update_user_usecase import UpdateUserUsecase
from src.modules.user.application.web.schemas.update_user_request_schema import UpdateUserRequestSchema

class UpdateUserController:

    def __init__(self, usecase: UpdateUserUsecase) -> None:
        self.usecase = usecase

    def __call__(
            self, 
            update_user: UpdateUserRequestSchema
            ) -> Any:

        return self.usecase(
            id = update_user.id,
            new_name = update_user.new_name,
            new_phone = update_user.new_phone,
            new_password = update_user.new_password,
            new_address = update_user.address
        )