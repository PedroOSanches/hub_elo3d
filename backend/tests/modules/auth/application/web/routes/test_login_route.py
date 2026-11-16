from fastapi.testclient import TestClient

from src.app.app import app
from pytest_bdd import given, then, when, scenario
from pathlib import Path

FEATURE_FILE = Path(__file__).parent.parent / 'features' / 'auth.feature'

@scenario(str(FEATURE_FILE), scenario_name='Login successful')
def test_login_route():
    pass

@given('that I have provided valid credentials', target_fixture='request_login')
def input_login():
    return {
        'email': 'user@example.com',
        'password': '!Teste123#'
    }

@when('I submit my login credentials', target_fixture='login_response')
def login(request_login):
    client = TestClient(app=app)
    return client.post(
        '/api/auth/login',
        json=request_login
    )

@then('I should successfully log in and access the EloHub 3D platform')
def login_sucessful(login_response):
    assert login_response.status_code == 200
    assert login_response.json()['message'] ==  'Login realizado com sucesso'

@then('authentication tokens are set in my cookies')
def client_receive_tokens(login_response):
    assert login_response.cookies.get('access_token') is not None
    assert login_response.cookies.get('refresh_token') is not None

@scenario(str(FEATURE_FILE), 'Unauthorized Login')
def test_login_unauthorized():
    pass

@given('that I have provided invalid credentials', target_fixture='request_login')
def input_invalid_credencials():
    return {
        'email': 'user@example.com',
        'password': 'teste123'
    }

@then('my login is not accept')
def unauthorized_response(login_response):
    assert login_response.status_code == 401
    assert login_response.json()['message'] ==  'Invalid email or password'

@then("authentication tokens aren't set in my cookies")
def unauthorized_response_cookies(login_response):
    assert login_response.cookies.get('access_token') is None
    assert login_response.cookies.get('refresh_token') is None

