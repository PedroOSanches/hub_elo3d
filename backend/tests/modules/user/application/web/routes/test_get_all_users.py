import pytest
import jwt
from src.app.app import app
from fastapi.testclient import TestClient
from datetime import datetime, timedelta, timezone
from src.modules.user.application.web.schemas.user_response_schema import UserResponseSchema

from src.modules.user.infra.repositories.user_repository_mock import UserRepositoryMock
from src.shared.environments.environments import env


@pytest.fixture
def get_access_token():
    now = datetime.now(timezone.utc)
    
    payload = {
        "sub": "b189d11a-25d1-430e-b5a1-c53db528337e",
        "email": "user@example.com",
        "role": "user",
        'type': 'access',
        "iat": now,
        "exp": now + timedelta(minutes=30),
    }

    return jwt.encode(
        payload,
        env.jwt_secret,
        algorithm='HS256'
    )

class Test_GetAllUsersRoute:

    def test_get_all_users(self, get_access_token):

        client = TestClient(app=app)
        client.cookies.set('access_token', value=get_access_token)
        response = client.get('api/user/get_all_users')

        all_users = UserRepositoryMock().get_all_users()

        
        all_users = [UserResponseSchema.model_validate(user).model_dump(mode='json') for user in all_users]


        assert response.status_code == 200
        assert response.json() == all_users

