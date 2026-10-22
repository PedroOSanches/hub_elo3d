import pytest

from fastapi.testclient import TestClient
from src.app.app import app
from src.modules.user.application.web.routes.create_user_route import create_router


def test_create_user():

    client = TestClient(app=app)

    created_user = client.post(
        'user/create',
        json={
            "name": "Pedro",
            "email":"pedro@aacd.com",
            "phone":"+5511999999999",
            "address": {
                "logradouro": "Rua Teste",
                'numero': "564",
                "bairro": "Novo Teste",
                'cidade':'Joateste',
                'estado': "SP",
                'cep': '00000-000',
                "complemento": "Casa"
            },
            'institution_id': "1cee6fe5-1fd5-4131-b054-4ec03358583a",
            'password': 'teste123@#$',
            'role': 'user_hospital'
        }
)
    assert created_user.status_code == 201
    assert created_user.json()['name'] == "Pedro"

def test_missing_parameter_user():

    client = TestClient(app=app)

    created_user = client.post(
        'user/create',
        json={
            "name": "Pedro",
            "email":"pedro@aacd.com",
            "address": {
                "logradouro": "Rua Teste",
                'numero': "564",
                "bairro": "Novo Teste",
                'cidade':'Joateste',
                'estado': "SP",
                'cep': '00000-000',
                "complemento": "Casa"
            },
            'institution_id': "1cee6fe5-1fd5-4131-b054-4ec03358583a",
            'password': 'teste123@#$',
            'role': 'user_hospital'
        }
)
    assert created_user.status_code == 400
    assert created_user.json()['message'] == "Field 'phone' is missing"

def test_missing_parameter_address():

    client = TestClient(app=app)

    created_user = client.post(
        'user/create',
        json={
            "name": "Pedro",
            "email":"pedro@aacd.com",
            'phone': '+5511999999999',
            "address": {
                "logradouro": "Rua Teste",
                'numero': "564",
                "bairro": "Novo Teste",
                'estado': "SP",
                'cep': '00000-000',
                "complemento": "Casa"
            },
            'institution_id': "1cee6fe5-1fd5-4131-b054-4ec03358583a",
            'password': 'teste123@#$',
            'role': 'user_hospital'
        }
)
    assert created_user.status_code == 400
    assert created_user.json()['message'] == "Field 'address.cidade' is missing"

def test_type_invalid_parameter():

    client = TestClient(app=app)

    created_user = client.post(
        'user/create',
        json={
            "name": "Pedro",
            "email":"pedro@aacd.com",
            'phone': 1,
            "address": {
                "logradouro": "Rua Teste",
                'numero': "564",
                "bairro": "Novo Teste",
                'cidade': 'Joateste',
                'estado': "SP",
                'cep': '00000-000',
                "complemento": "Casa"
            },
            'institution_id': "1cee6fe5-1fd5-4131-b054-4ec03358583a",
            'password': 'teste123@#$',
            'role': 'user_hospital'
        }
)
    assert created_user.status_code == 400
    assert created_user.json()['message'] == "The field 'phone' has the wrong type. Received: int. Expected: str"


def test_type_invalid_address_parameter():

    client = TestClient(app=app)

    created_user = client.post(
        'user/create',
        json={
            "name": "Pedro",
            "email":"pedro@aacd.com",
            'phone': '+5511900000000',
            "address": {
                "logradouro": "Rua Teste",
                'numero': "564",
                "bairro": "Novo Teste",
                'cidade': 'Joateste',
                'estado': "SP",
                'cep': '00000-000',
                "complemento": [123]
            },
            'institution_id': "1cee6fe5-1fd5-4131-b054-4ec03358583a",
            'password': 'teste123@#$',
            'role': 'user_hospital'
        }
)
    assert created_user.status_code == 400
    assert created_user.json()['message'] == "The field 'complemento' has the wrong type. Received: list. Expected: str"