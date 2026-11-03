from typing import Any

from src.modules.auth.application.usecases.refresh_token_usecase import RefreshTokenUsecase
from src.modules.auth.domain.errors.auth_error_usecase import AuthUnathorizedAction
from src.modules.auth.application.web.schemas.refresh_token_response_schema import RefreshTokenResponseSchema


class RefreshTokenController:

    def __init__(self, usecase: RefreshTokenUsecase) -> None:
        self.usecase = usecase

    def __call__(self, *, refresh_token: str | None) -> RefreshTokenResponseSchema:

        if refresh_token is None:
            raise AuthUnathorizedAction()

        return self.usecase(refresh_token=refresh_token)