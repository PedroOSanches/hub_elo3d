import pytest
from datetime import datetime, timedelta, timezone

from fastapi.testclient import TestClient
import jwt
from src.app.app import app
from src.shared.environments import env

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

class Test_UpdateUserRoute:

    def test_update_user_route(self, get_access_token):

        client = TestClient(app=app)

        client.cookies.set("access_token", get_access_token)
        response = client.post(
            '/api/user/update_user',
            json={
                "user_id": "20ba02d0-d00f-474b-ad43-10b76abba8ee",
                "new_name": "Luiza"
            }
        )

        assert response.status_code == 200
        assert response.json() == {
            'user_id': '20ba02d0-d00f-474b-ad43-10b76abba8ee', 
            'name': 'Luiza', 
            'email': 'user@aacd.com', 
            'phone': 'tel:+55-11-99999-9999', 
            'address': {
                'logradouro': 'Rua Teste', 
                'numero': 'S/N', 
                'bairro': 'Teste', 
                'cidade': 'São Teste do Sul', 
                'estado': 'SP', 
                'cep': '00000-000', 
                'complemento': 'Casa'
                },
            'institution_id': None,
            'role': 'hospital'
            }

    def test_not_found_user(self, get_access_token):
        client = TestClient(app=app)
        client.cookies.set('access_token', get_access_token)
        response = client.post(
            '/api/user/update_user',
            json={
                "user_id": "b189d12a-25d1-430e-b5a1-c53db528337e",
                "new_name": "Luiza"
            }
        )
        
        assert response.status_code == 404
        assert response.json()['message'] == 'No users found for user_id: b189d12a-25d1-430e-b5a1-c53db528337e'
    
    def test_type_invalid(self, get_access_token):
        client = TestClient(app=app)
        client.cookies.set('access_token', get_access_token)
        response = client.post(
            '/api/user/update_user',
            json={
                "user_id": "b189d12a-25d1-430e-b5a1-c53db528337e",
                "new_name": 1
            }
        )
        
        assert response.status_code == 400
        assert response.json()['message'] == "The field 'new_name' has the wrong type. Received: int. Expected: str | None"
