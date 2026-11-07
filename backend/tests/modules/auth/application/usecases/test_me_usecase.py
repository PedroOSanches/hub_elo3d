from uuid import uuid7

import pytest
from src.modules.auth.application.usecases.me_usecase import MeUsecase
from src.modules.auth.domain.entities.auth_user import AuthUser
from src.modules.auth.infra.security.jwt_service import JWTService
from src.shared.environments.environments import env

@pytest.fixture
def get_access_token():

    return JWTService(jwt_secret=env.jwt_secret).get_access_token(AuthUser(
        user_id=uuid7(),
        email='user@example.com',
        password_hash='HASH_PASSWORD',
        role='user_hospital'
    ))

@pytest.fixture
def usecase():

    return MeUsecase(jwt_service=JWTService(jwt_secret=env.jwt_secret))

class Test_MeUsecase:

    def test_me_usecase(self, get_access_token, usecase):

        user = usecase(access_token=get_access_token)

        assert user.role == 'user_hospital'