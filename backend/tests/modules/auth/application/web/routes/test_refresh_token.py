import pytest
from fastapi.testclient import TestClient

import jwt
from uuid import UUID
from src.app.app import app
from src.shared.environments import env
from src.modules.auth.infra.security.jwt_service import JWTService
from src.modules.auth.domain.entities.auth_user import AuthUser

@pytest.fixture
def get_refresh_token():

    return JWTService(jwt_secret=env.jwt_secret).get_refresh_token(user=AuthUser(
        user_id=UUID('b189d11a-25d1-430e-b5a1-c53db528337e'),
        email='user@example.com',
        password_hash='HASH_SENHA',
        role='user'
    ))

class Test_RefreshTokenRoute:

    def test_refresh_token_route(self, get_refresh_token):

        client = TestClient(app=app)

        client.cookies.set('refresh_token', get_refresh_token)

        response = client.post(
            '/api/auth/refresh',
            json={}
        )

        assert response.status_code == 200
        assert response.json() == {'message': 'New access_token created'}

    def test_refresh_token_invalid_token(self, get_refresh_token):

        client = TestClient(app=app)

        client.cookies.set('refresh_token', 'AA')

        response = client.post(
            '/api/auth/refresh',
            json={}
        )

        assert response.status_code == 401
        assert response.json() == {'message': 'Authentication Failed'}