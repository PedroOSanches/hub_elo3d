import pytest

from fastapi.testclient import TestClient
from src.app.app import app


def test_create_user():

    client = TestClient(app=app)

    created_user = client.post(
        'api/user/create',
        json={
            "name": "Pedro",
            "email":"pedro@aacd.com",
            "phone":"+5511999999999",
            "address": {
                "street": "Rua Teste",
                'number': "564",
                "neighborhood": "Novo Teste",
                'city':'Joateste',
                'state': "SP",
                'cep': '00000-000',
                "address_details": "Casa"
            },
            'password': '!Teste123@#$',
            'role': 'user_hospital'
        }
)
    assert created_user.status_code == 201
    assert created_user.json()['name'] == "Pedro"

def test_missing_parameter_user():

    client = TestClient(app=app)

    created_user = client.post(
        'api/user/create',
        json={
            "name": "Pedro",
            "email":"pedro@aacd.com",
            "address": {
                "street": "Rua Teste",
                'number': "564",
                "neighborhood": "Novo Teste",
                'city':'Joateste',
                'state': "SP",
                'cep': '00000-000',
                "address_details": "Casa"
            },
            'password': '!Teste123@#$',
            'role': 'user_hospital'
        }
)
    assert created_user.status_code == 400
    assert created_user.json()['message'] == "Field 'phone' is missing"

def test_missing_parameter_address():

    client = TestClient(app=app)

    created_user = client.post(
        'api/user/create',
        json={
            "name": "Pedro",
            "email":"pedro@aacd.com",
            'phone': '+5511999999999',
            "address": {
                "street": "Rua Teste",
                'number': "564",
                "neighborhood": "Novo Teste",
                'state': "SP",
                'cep': '00000-000',
                "address_details": "Casa"
            },
            'password': '!Teste123@#$',
            'role': 'user_hospital'
        }
)
    assert created_user.status_code == 400
    assert created_user.json()['message'] == "Field 'address.city' is missing"

def test_type_invalid_parameter():

    client = TestClient(app=app)

    created_user = client.post(
        'api/user/create',
        json={
            "name": "Pedro",
            "email":"pedro@aacd.com",
            'phone': 1,
            "address": {
                "street": "Rua Teste",
                'number': "564",
                "neighborhood": "Novo Teste",
                'city': 'Joateste',
                'state': "SP",
                'cep': '00000-000',
                "address_details": "Casa"
            },
            'password': '!Teste123@#$',
            'role': 'user_hospital'
        }
)
    assert created_user.status_code == 400
    assert created_user.json()['message'] == "The field 'phone' has the wrong type. Received: int. Expected: str"


def test_type_invalid_address_parameter():

    client = TestClient(app=app)

    created_user = client.post(
        'api/user/create',
        json={
            "name": "Pedro",
            "email":"pedro@aacd.com",
            'phone': '+5511900000000',
            "address": {
                "street": "Rua Teste",
                'number': "564",
                "neighborhood": "Novo Teste",
                'city': 'Joateste',
                'state': "SP",
                'cep': '00000-000',
                "address_details": [123]
            },
            'password': '!Teste123@#$',
            'role': 'user_hospital'
        }
)
    assert created_user.status_code == 400
    assert created_user.json()['message'] == "The field 'address_details' has the wrong type. Received: list. Expected: str | None"
