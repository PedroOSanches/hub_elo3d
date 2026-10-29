import pytest

from src.modules.auth.application.usecases.refresh_token_usecase import RefreshTokenUsecase, GatewayUser, JWTService
from src.modules.auth.domain.errors.auth_error_usecase import AuthUnathorizedAction
from src.modules.user.infra.repositories.user_repository_mock import UserRepositoryMock
from src.shared.environments import env

@pytest.fixture
def jwt_service():
    return JWTService(jwt_secret=env.jwt_secret)

@pytest.fixture
def gateway():
    return GatewayUser(repo=UserRepositoryMock())

@pytest.fixture
def get_refresh_token(jwt_service, gateway):
    user = gateway.get_user_by_email('user@example.com')
    return jwt_service.get_refresh_token(user=user)

@pytest.fixture
def usecase(gateway, jwt_service):
    return RefreshTokenUsecase(gateway_user=gateway, jwt_service=jwt_service)


class Test_RefreshTokenUsecase:

    def test_refresh_token_usecase(self, usecase, get_refresh_token, jwt_service):

        response = usecase(refresh_token=get_refresh_token)

        payload = jwt_service.decode_token(token=response.access_token)

        assert payload.get('email') == 'user@example.com'
        assert payload.get('role') == 'user'
    
    def test_refresh_token_usecase_invalid_token(self, usecase, get_refresh_token, jwt_service):

        with pytest.raises(AuthUnathorizedAction):
            usecase(
                refresh_token='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJiMTg5ZDExYS0yNWQxLTQzMGUtYjVhMS1jNTNkYjUyODMzN2UiLCJ0eXBlIjoicmVmcmVzaCIsImlhdCI6MTc5MzIzMTA1MCwiZXhwIjoxNzkzMTE3NDQ4fQ.W2xFNz6XHzvX7opjbC3JbSY6icCJQOUucKR-QiO1UE4'
                )

    def test_refresh_token_not_jwt(self, usecase):
        with pytest.raises(AuthUnathorizedAction):
            usecase(refresh_token=4)