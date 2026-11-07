import pytest
from datetime import datetime, timedelta, timezone

from fastapi.testclient import TestClient
import jwt
from src.app.app import app
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


class Test_DeleteUser:

    def test_delete_user(self, get_access_token):

        client = TestClient(app=app)
        client.cookies.set('access_token', get_access_token)

        deleted_user = client.delete(
        'api/user/delete_user/b189d11a-25d1-430e-b5a1-c53db528337e'
        )

        assert deleted_user.status_code == 200
        assert deleted_user.json()['name'] == 'User'
    
    def test_delete_user_not_found_user(self, get_access_token):

        client = TestClient(app=app)
        client.cookies.set('access_token', get_access_token)

        deleted_user = client.delete(
        'api/user/delete_user/b189d21a-25d1-430e-b5a1-c53db528337e'
        )


        assert deleted_user.status_code == 404
        assert deleted_user.json()['message'] == 'No users found for user_id: b189d21a-25d1-430e-b5a1-c53db528337e'

    def test_delete_user_type_id_invalid(self, get_access_token):

        client = TestClient(app=app)
        client.cookies.set('access_token', get_access_token)

        response = client.delete(
            "api/user/delete_user/1234"
        )

        assert response.status_code == 400
        assert response.json()['message'] == "The field 'user_id' has the wrong type. Received: str. Expected: UUID"