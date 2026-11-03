import pytest
from src.modules.auth.domain.entities.auth_user import AuthUser
from src.modules.auth.infra.security.jwt_service import JWTService
from src.modules.user.infra.repositories.user_repository_mock import UserRepositoryMock
from src.shared.environments import env
from uuid import UUID

@pytest.fixture
def auth_user() -> AuthUser:
    return AuthUser(
        user_id=UUID('b189d11a-25d1-430e-b5a1-c53db528337e'),
        email='user@example.com',
        password_hash="!Teste123#",
        role='user'
    )

@pytest.fixture
def jwt_service() -> JWTService:
    return JWTService(jwt_secret=env.jwt_secret)

class Test_JWTService:

    def test_jwt_service_get_access_token(self, auth_user, jwt_service):
        access_token = jwt_service.get_access_token(auth_user)

        payload = jwt_service.decode_token(token=access_token)

        assert payload.get('role') == 'user'

    def test_jwt_service_get_refresh_token(self, jwt_service, auth_user):

        refresh_token = jwt_service.get_refresh_token(
            auth_user
        )

        payload = jwt_service.decode_token(token=refresh_token)

        assert payload.get('sub') == str(auth_user.user_id)