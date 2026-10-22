import pytest
from fastapi.testclient import TestClient
from src.app.app import app

class Test_GetUserRouter:

    def test_get_user(self):

        client = TestClient(app=app)

        get_user = client.get(
            '/user/get_user/b189d11a-25d1-430e-b5a1-c53db528337e',
        )

        response = get_user.json()

        assert get_user.status_code  == 200
        assert response['name'] == 'User'
        assert response['email'] == 'user@example.com'
        assert response['role'] == 'user'

    def test_not_found_user(self):

        client = TestClient(app=app)

        get_user = client.get(
            '/user/get_user/51b867a2-2c1d-4816-9213-7768c1e71c88',
        )

        response = get_user.json()
        assert get_user.status_code  == 404
        assert response['message'] == "No users found for id: '51b867a2-2c1d-4816-9213-7768c1e71c88'"

    def test_id_type_invalid(self):

        client = TestClient(app=app)

        get_user = client.get(
            '/user/get_user/a'
        )

        assert get_user.status_code == 400
        assert get_user.json() == {
            'message': "The field 'id' has the wrong type. Received: str. Expected: UUID"
        }