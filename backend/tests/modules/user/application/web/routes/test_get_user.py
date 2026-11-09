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




class Test_GetUserRouter:

    def test_get_user(self, get_access_token):

        client = TestClient(app=app)
        client.cookies.set('access_token', get_access_token)
        
        get_user = client.get(
            '/api/user/get_user/20ba02d0-d00f-474b-ad43-10b76abba8ee',
        )

        response = get_user.json()

        assert get_user.status_code  == 200
        assert response['name'] == 'User AACD'
        assert response['email'] == 'user@aacd.com'
        assert response['role'] == 'hospital'

    def test_no_found_user(self, get_access_token):

        client = TestClient(app=app)
        client.cookies.set('access_token', get_access_token)

        get_user = client.get(
            '/api/user/get_user/51b867a2-2c1d-4816-9213-7768c1e71c88',
        )

        response = get_user.json()
        assert get_user.status_code  == 404
        assert response['message'] == "No users found for user_id: 51b867a2-2c1d-4816-9213-7768c1e71c88"

    def test_id_type_invalid(self, get_access_token):

        client = TestClient(app=app)
        client.cookies.set('access_token', get_access_token)

        get_user = client.get(
            '/api/user/get_user/a'
        )

        assert get_user.status_code == 400
        assert get_user.json() == {
            'message': "The field 'user_id' has the wrong type. Received: str. Expected: UUID"
        }