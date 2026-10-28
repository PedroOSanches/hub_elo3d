import jwt
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from src.modules.auth.domain.gateways.gateway_user_interface import IGatewayUser, AuthUser
from src.modules.auth.domain.errors.auth_error_usecase import InvalidCredentials
from src.shared.utils.password_hasher import verificar_senha


@dataclass
class AuthTokensDTO:
    access_token: str
    refresh_token: str
    token_type: str = 'bearer'


class LoginUsecase:

    def __init__(self, gateway: IGatewayUser, jwt_secret: str) -> None:
        self.gateway = gateway
        self.jwt_secret = jwt_secret

    def __call__(self, *, email: str, password: str) ->  AuthTokensDTO:
            
            user = self.gateway.get_user_by_email(email=email)

            if not verificar_senha(password, user.password_hash):
                raise InvalidCredentials()
            
            access_token = self._get_access_token(user=user)
            refresh_token = self._get_refresh_token(user=user)

            return AuthTokensDTO(
                access_token=access_token,
                refresh_token=refresh_token
            )        

    def _get_access_token(self, user: AuthUser):
        now = datetime.now(timezone.utc)

        payload = {
            'sub': str(user.id),
            'email': user.email,
            'role': user.role,
            'iat': now,
            'exp': now + timedelta(minutes=30)
        }

        return jwt.encode(
            payload=payload,
            key=self.jwt_secret,
            algorithm='HS256'
        )

    def _get_refresh_token(self, user: AuthUser):
        now = datetime.now(timezone.utc)

        payload = {
            'sub': str(user.id),
            'type': 'refresh',
            'iat': now,
            'exp': now + timedelta(days=3)
        }

        return jwt.encode(
            payload=payload,
            key=self.jwt_secret,
            algorithm='HS256'
        )