from typing import Any

from uuid import UUID
from src.modules.auth.infra.security.jwt_service import JWTService
from src.modules.auth.infra.external.gateways.gateway_user import GatewayUser
from src.modules.auth.application.web.schemas.refresh_token_response_schema import RefreshTokenResponseSchema


class RefreshTokenUsecase:

    def __init__(
            self,
            *,
            gateway_user: GatewayUser,
            jwt_service: JWTService
            ) -> None:
        self.gateway_user = gateway_user
        self.jwt_service = jwt_service


    def __call__(self, *, refresh_token: str) -> RefreshTokenResponseSchema:

        user_id = UUID(self.jwt_service.validate_refresh_token(refresh_token=refresh_token))
        user = self.gateway_user.get_user_by_id(user_id=user_id)
        access_token = self.jwt_service.get_access_token(
            user=user
        )

        return RefreshTokenResponseSchema(
            access_token=access_token
        )

