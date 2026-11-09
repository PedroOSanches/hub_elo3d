import pytest
from src.modules.user.application.web.schemas.create_user_schema import (
    CreateUserRequestSchema, 
    Address, 
    MissingParameters, 
    WrongTypeParameter
)

from src.modules.user.application.web.schemas.user_response_schema import UserResponseSchema


class Test_CreateUserRequestSchema:


    def test_create_user_request_schema(self):

        request = {
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
                "address_details": ""
            },
            'password': '!!Teste123@#$',
            'role': 'hospital'
        }

        create_user_request_schema = CreateUserRequestSchema(**request)

    def test_name_missing(self):
        with pytest.raises(MissingParameters):
            request = {
                        "email":"pedro@aacd.com",
                        "phone":"+5511999999999",
                        "address": {
                            "street": "Rua Teste",
                            'number': "564",
                            "neighborhood": "Novo Teste",
                            'city':'Joateste',
                            "address_details": "",
                            'state': "SP",
                            'cep': '00000-000'
                        },
                        'password': '!!Teste123@#$',
                        'role': 'hospital'
                    }
            request = CreateUserRequestSchema(**request)

    def test_email_missing(self):
        with pytest.raises(MissingParameters):
            request = {
                        'name': "Pedro",
                        "phone":"+5511999999999",
                        "address": {
                            "street": "Rua Teste",
                            'number': "564",
                            "neighborhood": "Novo Teste",
                            'city':'Joateste',
                            "address_details": "",
                            'state': "SP",
                            'cep': '00000-000'
                        },
                        'password': '!Teste123@#$',
                        'role': 'hospital'
                    }
            CreateUserRequestSchema(**request)

    def test_address_missing_missing(self):
        with pytest.raises(MissingParameters):
            request = {
                        'name': "Pedro",
                        "phone": "+5511999999999",
                        'password': '!Teste123@#$',
                        'role': 'hospital'
                    }
            CreateUserRequestSchema(**request) # pyright: ignore[reportArgumentType]

    def test_name_type_invalid(self):
        with pytest.raises(WrongTypeParameter):
            request = {
                "name": 1,
                "email":"pedro@aacd.com",
                "phone":"+5511999999999",
                "address": {
                    "street": "Rua Teste",
                    'number': "564",
                    "neighborhood": "Novo Teste",
                    'city':'Joateste',
                    'state': "SP",
                    'cep': '00000-000',
                    "address_details": ""
                    },
                'password': '!Teste123@#$',
                'role': 'hospital'
                }
                
            create_user_request_schema = CreateUserRequestSchema(**request)
    def test_email_type_invalid(self):

        with pytest.raises(WrongTypeParameter):
            request = {
                "name": "Pedro",
                "email": 1,
                "phone":"+5511999999999",
                "address": {
                    "street": "Rua Teste",
                    'number': "564",
                    "neighborhood": "Novo Teste",
                    'city':'Joateste',
                    'state': "SP",
                    'cep': '00000-000',
                    "address_details": ""
                    },
                'password': '!Teste123@#$',
                'role': 'hospital'
                }
                
            create_user_request_schema = CreateUserRequestSchema(**request)

    def test_phone_type_invalid(self):

        with pytest.raises(WrongTypeParameter):
            request = {
                "name": "Pedro",
                "email":"pedro@aacd.com",
                "phone":123,
                "address": {
                    "street": "Rua Teste",
                    'number': "564",
                    "neighborhood": "Novo Teste",
                    'city':'Joateste',
                    'state': "SP",
                    'cep': '00000-000',
                    "address_details": ""
                    },
                'password': '!Teste123@#$',
                'role': 'hospital'
                }
                
            create_user_request_schema = CreateUserRequestSchema(**request)

    def test_password_type_invalid(self):

        with pytest.raises(WrongTypeParameter):
            request = {
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
                    "address_details": ""
                    },
                'password': 123455,
                'role': 'hospital'
                }
                
            create_user_request_schema = CreateUserRequestSchema(**request)

    def test_address_type_invalid(self):
        with pytest.raises(WrongTypeParameter):
            request = {
                "name": "Pedro",
                "email":"pedro@aacd.com",
                "phone":"+5511999999999",
                "address": ["Rua teste", "564"],
                'password': '!Teste123@#$',
                'role': 'hospital'
                    }
                    
            create_user_request_schema = CreateUserRequestSchema(**request)

    def test_role_type_invalid(self):

        with pytest.raises(WrongTypeParameter):
            request = {
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
                    "address_details": ""
                    },
                'password': '!Teste123@#$',
                'role': 'felipe'
                }
                
            create_user_request_schema = CreateUserRequestSchema(**request)