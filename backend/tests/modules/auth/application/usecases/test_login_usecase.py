import pytest

from src.modules.auth.application.usecases.login_usecase import LoginUsecase
from src.modules.auth.infra.external.gateways.gateway_user import GatewayUser
from src.modules.auth.infra.security.jwt_service import JWTService
from src.modules.user.infra.repositories.user_repository_mock import UserRepositoryMock
from src.shared.environments import env
from src.shared.errors.usecase_error import NotFoundError

@pytest.fixture
def usecase():
    jwt_service = JWTService(jwt_secret=env.jwt_secret)
    repo = UserRepositoryMock()
    gateway = GatewayUser(repo=repo)
    return LoginUsecase(gateway=gateway, jwt_service=jwt_service)

@pytest.fixture
def jwt_service():
    return JWTService(jwt_secret=env.jwt_secret)

class Test_LoginUsecase:

    def test_login_usecase(self, usecase, jwt_service):
        user = usecase(email='user@example.com', password='!Teste123#')

        payload = jwt_service.decode_token(token=user.access_token)

        assert user.access_token is not None and user.refresh_token is not None
        assert payload.get('role') == 'user'
    
    def test_login_invalid_credentials(self, usecase, jwt_service):

        with pytest.raises(NotFoundError):
            usecase(email='user@example.com.br', password='!Teste123#')