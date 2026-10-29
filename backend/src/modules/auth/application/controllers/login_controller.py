from typing import Any

from src.modules.auth.application.usecases.login_usecase import LoginUsecase, AuthTokensDTO
from src.modules.auth.application.web.schemas.login_schema import LoginRequestSchema
from src.modules.auth.domain.errors.auth_error_usecase import InvalidCredentials
from src.shared.errors.usecase_error import NotFoundError
class LoginController:

    def __init__(self, usecase: LoginUsecase) -> None:
        self.usecase = usecase

    def __call__(self, request: LoginRequestSchema) -> AuthTokensDTO:
        try:
            return self.usecase(
                email=request.email,
                password=request.password
            )
        except NotFoundError:
            raise InvalidCredentials()