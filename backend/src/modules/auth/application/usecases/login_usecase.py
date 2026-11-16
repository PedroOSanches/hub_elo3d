from dataclasses import dataclass

from src.modules.auth.domain.errors.auth_error_usecase import InvalidCredentials
from src.modules.auth.domain.gateways.gateway_user_interface import (
    IGatewayUser,
)
from src.modules.auth.infra.security.jwt_service import JWTService
from src.shared.utils.password_hasher import verificar_senha


@dataclass
class AuthTokensDTO:
    access_token: str
    refresh_token: str

class LoginUsecase:

    def __init__(self, gateway: IGatewayUser, jwt_service: JWTService) -> None:
        self.gateway = gateway
        self.jwt_service = jwt_service

    def __call__(self, *, email: str, password: str) ->  AuthTokensDTO:
            
            user = self.gateway.get_user_by_email(email=email)

            if not verificar_senha(password, user.password_hash):
                raise InvalidCredentials()
            
            access_token = self.jwt_service.get_access_token(user=user)
            refresh_token = self.jwt_service.get_refresh_token(user=user)

            return AuthTokensDTO(
                access_token=access_token,
                refresh_token=refresh_token
            )