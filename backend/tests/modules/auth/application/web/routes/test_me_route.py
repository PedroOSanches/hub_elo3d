from uuid import UUID, uuid7

from fastapi.testclient import TestClient
import pytest

from src.app.app import app
from src.modules.auth.domain.entities.auth_user import AuthUser
from src.modules.auth.infra.security.jwt_service import JWTService
from src.shared.environments import env


@pytest.fixture
def get_access_token() -> str:
    
    return JWTService(jwt_secret=env.jwt_secret).get_access_token(user=AuthUser(
        user_id=uuid7(),
        email='user@example.com',
        password_hash='HASH_SENHA',
        role='hospital'
    ))

class Test_MeRoute:


    def test_me_route(self, get_access_token):

        client = TestClient(app=app)
        client.cookies.set('access_token', get_access_token)

        me_route = client.get(
            '/api/auth/me'
        )

        print(me_route.json())
        assert me_route.json().get('role') == 'hospital'


