import jwt
from jwt import InvalidTokenError
from datetime import datetime, timedelta, timezone
from src.modules.auth.domain.entities.auth_user import AuthUser
from src.modules.auth.domain.errors.auth_error_usecase import AuthUnathorizedAction


class JWTService:

    ALGORITHM = 'HS256'

    def __init__(
            self,
            *,
            jwt_secret: str,
            access_token_exp_minutes: int = 60,
            refresh_token_exp_days: int = 1
            ) -> None:
        self.jwt_secret = jwt_secret
        self.access_token_exp_minutes = access_token_exp_minutes
        self.refresh_token_exp_days = refresh_token_exp_days



    def get_access_token(self, user: AuthUser) -> str:
        now = datetime.now(timezone.utc)

        payload = {
            'sub': str(user.user_id),
            'email': user.email,
            'role': user.role,
            'iat': now,
            'exp': (now + timedelta(minutes=self.access_token_exp_minutes))
        }

        return jwt.encode(
            payload=payload,
            key=self.jwt_secret,
            algorithm= self.ALGORITHM
        )

    def get_refresh_token(self, user: AuthUser) -> str:
        now = datetime.now(timezone.utc)

        payload = {
            'sub': str(user.user_id),
            'type': 'refresh',
            'iat': now,
            'exp': (now + timedelta(days=self.refresh_token_exp_days))
        }

        return jwt.encode(
            payload=payload,
            key=self.jwt_secret,
            algorithm= self.ALGORITHM
        )


    def validate_refresh_token(self, refresh_token: str):
        try:
            payload = self.decode_token(token=refresh_token)

            if payload.get('type') != 'refresh':
                raise ValueError('Invalid token type')

            user_id = payload.get('sub')

            if not isinstance(user_id, str) or not user_id: 
                raise ValueError('Invalid token subject')

            return user_id
        except (InvalidTokenError, ValueError) as err:
            raise AuthUnathorizedAction()

    def decode_token(self, *, token: str) -> dict:
        return jwt.decode(
            token,
            self.jwt_secret,
            algorithms=[self.ALGORITHM]
        )