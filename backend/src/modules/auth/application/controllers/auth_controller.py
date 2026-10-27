from typing import Any

from src.modules.auth.application.usecases.auth_usecase import AuthUsecase
from src.modules.auth.application.web.schemas.auth_schema import AuthRequestSchema

class AuthController:

    def __init__(self, usecase: AuthUsecase) -> None:
        self.usecase = usecase

    def __call__(self, request: AuthRequestSchema) -> Any:
        return self.usecase(
            email=request.email,
            password=request.password
        )