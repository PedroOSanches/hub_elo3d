from fastapi.testclient import TestClient
from src.app.app import app


class Test_UpdateUserRoute:

    def test_update_user_route(self):

        client = TestClient(app=app)

        response = client.post(
            'user/update_user',
            json={
                "id": "b189d11a-25d1-430e-b5a1-c53db528337e",
                "new_name": "Luiza"
            }
        )

        assert response.status_code == 200
        assert response.json() == {
            'id': 'b189d11a-25d1-430e-b5a1-c53db528337e', 
            'name': 'Luiza', 
            'email': 'user@example.com', 
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
            'institution_id': None
            }

    def test_not_found_user(self):
        client = TestClient(app=app)
        
        response = client.post(
            'user/update_user',
            json={
                "id": "b189d12a-25d1-430e-b5a1-c53db528337e",
                "new_name": "Luiza"
            }
        )

        print(response.json())

        assert response.status_code == 404
