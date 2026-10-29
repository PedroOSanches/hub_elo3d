import pytest
from src.modules.auth.application.controllers.refresh_token_controller import RefreshTokenController
from src.modules.auth.application.usecases.refresh_token_usecase import RefreshTokenUsecase
from src.modules.auth.infra.external.gateways.gateway_user import GatewayUser
from src.modules.auth.infra.security.jwt_service import JWTService
from src.modules.user.infra.repositories.user_repository_mock import UserRepositoryMock
from src.modules.auth.domain.errors.auth_error_usecase import AuthUnathorizedAction
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
def controller(gateway, jwt_service):
    usecase = RefreshTokenUsecase(gateway_user=gateway, jwt_service=jwt_service)
    return RefreshTokenController(usecase=usecase)

class Test_RefreshTokenController:

    def test_refresh_token_controller(self, controller, get_refresh_token, jwt_service):

        response = controller(refresh_token=get_refresh_token)

        print(get_refresh_token)
        
        payload = jwt_service.decode_token(token=response.access_token)

        assert response.access_token is not None
        assert payload.get('role') == 'user'
    
    def test_refresh_token_controller_invalid_token(self, controller):

        with pytest.raises(AuthUnathorizedAction):
            controller(
                refresh_token='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJiMTg5ZDExYS0yNWQxLTQzMGUtYjVhMS1jNTNkYjUyODMzN2UiLCJ0eXBlIjoicmVmcmVzaCIsImlhdCI6MTc5MzIzMTA1MCwiZXhwIjoxNzkzMTE3NDQ4fQ.W2xFNz6XHzvX7opjbC3JbSY6icCJQOUucKR-QiO1UE4'
                )
    
    def test_refresh_token_controller_missing_token(self, controller):

        with pytest.raises(AuthUnathorizedAction):
            controller(
                refresh_token=None
                )