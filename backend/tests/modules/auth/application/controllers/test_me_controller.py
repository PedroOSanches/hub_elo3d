from uuid import UUID

import pytest

from src.modules.auth.application.controllers.me_controller import MeController
from src.modules.auth.application.usecases.me_usecase import MeUsecase
from src.modules.auth.domain.entities.auth_user import AuthUser
from src.modules.auth.infra.external.gateways.gateway_user import GatewayUser
from src.modules.auth.infra.security.jwt_service import JWTService
from src.shared.environments import env

@pytest.fixture
def controller():
    jwt_service = JWTService(jwt_secret=env.jwt_secret)
    gateway_user = GatewayUser(GatewayUser.get_repo_user())
    usecase = MeUsecase(jwt_service=jwt_service)
    return MeController(usecase=usecase)



class Test_MeController:

    def test_me_controller(self, controller):

        jwt_service = JWTService(jwt_secret=env.jwt_secret)

        access_token = jwt_service.get_access_token(
            AuthUser(
                user_id=UUID('20ba02d0-d00f-474b-ad43-10b76abba8ee'),
                email='user_example@gmail.com',
                password_hash='HASH_SENHA',
                role='user'
            )
        )

        user = controller(access_token=access_token)