from fastapi.testclient import TestClient
from src.app.app import app




class Test_LoginRoute:


    def test_login_route(self):
        client = TestClient(app=app)
        request = {
            'email': 'user@example.com',
            'password': '!Teste123#'
        }

        response = client.post(
            '/api/auth/login',
            json=request
        )

        assert response.status_code == 200
        assert response.cookies.get('access_token') is not None
        assert response.cookies.get('refresh_token') is not None
        assert response.json()['message'] ==  'Login realizado com sucesso'


    def test_login_unauthorized(self):
        client = TestClient(app=app)
        request = {
            'email': 'user@example.com',
            'password': 'teste123'
        }

        response = client.post(
            '/api/auth/login',
            json=request
        )

        print(response.json())
        assert response.status_code == 401
        assert response.cookies.get('access_token') is None
        assert response.cookies.get('refresh_token') is None
        assert response.json()['message'] ==  'Invalid email or password'