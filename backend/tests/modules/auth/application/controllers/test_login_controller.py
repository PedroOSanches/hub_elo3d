import pytest
from src.modules.auth.application.controllers.login_controller import LoginController, InvalidCredentials
from src.modules.auth.application.usecases.login_usecase import LoginUsecase
from src.modules.auth.infra.external.gateways.gateway_user import GatewayUser
from src.modules.auth.infra.security.jwt_service import JWTService
from src.modules.auth.application.web.schemas.login_schema import LoginRequestSchema

from src.shared.environments import env
@pytest.fixture
def controller():
    gateway = GatewayUser(env.repo_user)
    jwt_service = JWTService(jwt_secret=env.jwt_secret)
    usecase = LoginUsecase(gateway=gateway, jwt_service=jwt_service)
    return LoginController(usecase=usecase)

@pytest.fixture
def jwt_service():
    return JWTService(jwt_secret=env.jwt_secret)

class Test_LoginController:

    def test_login_controller(self, controller, jwt_service):
        request = LoginRequestSchema(
            email='user@example.com',
            password='!Teste123#'
        )

        tokens = controller(request=request)

        access_token_payload = jwt_service.decode_token(token=tokens.access_token)

        assert tokens.access_token is not None
        assert access_token_payload.get('email') is not None
        assert access_token_payload.get('role') == 'user'
    
    def test_login_controller_invalid_credentials(self, controller, jwt_service):
        request = LoginRequestSchema(
            email='invalid_credentials@example.com',
            password='!Teste123#'
        )

        with pytest.raises(InvalidCredentials):
            tokens = controller(request=request)