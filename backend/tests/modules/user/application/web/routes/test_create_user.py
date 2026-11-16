import pytest

from fastapi.testclient import TestClient
from src.app.app import app
from pytest_bdd import scenario, given, then, when
from pathlib import Path
FEATURE_FILE = Path(__file__).parent / 'features' / 'user.feature'

@scenario(str(FEATURE_FILE), scenario_name='Partner registration')
def test_create_user():
    pass


@given(
        'that I have provided valid information',
        target_fixture='registration_information'
        )
def valid_information():
    return {
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

@when('I submit my registration', target_fixture='registration_response')
def create_user(registration_information):

    client = TestClient(app=app)
    return client.post(
        'api/user/create',
        json=registration_information
)

@then('my user account should be created')
def verify_partner_registration(registration_response):
    assert registration_response.status_code == 201
    assert registration_response.json()['name'] == "Pedro"

@scenario(str(FEATURE_FILE), scenario_name='Partner registration fails due to missing parameters')
def test_missing_parameter_user():
    pass


@given('that I have provided informations with missing parameters', target_fixture='registration_information')
def invalid_input_missing_parameter():
    return {
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

@then('my user accound should not be created')
def status_code_error_missing_parameter(registration_response):
    assert registration_response.status_code == 400

@then('I should receive an error message missing parameter')
def error_missing_parameter(registration_response):
    assert registration_response.json()['message'] == "Field 'phone' is missing"

@scenario(str(FEATURE_FILE), scenario_name='Partner registration fails due to wrong type parameters')
def test_type_invalid_parameter():
    pass

@given('that I have provided informations with wrong type parameters', target_fixture='registration_information')
def input_wrong_type_parameter():
    return {
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

@then('I should receive an error message wrong parameter')
def wrong_type_parameter_error(registration_response):
    assert registration_response.json()['message'] == "The field 'phone' has the wrong type. Received: int. Expected: str"

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

def test_type_invalid_institution():

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
                'city': 'Joateste',
                'state': "SP",
                'cep': '00000-000',
                "address_details": "Casa"
            },
            'institution_id': 12,
            'password': '!Teste123@#$',
            'role': 'user_hospital'
        }
)
    assert created_user.status_code == 400
    assert created_user.json()['message'] == "The field 'institution_id' has the wrong type. Received: int. Expected: uuid.UUID | None"


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
