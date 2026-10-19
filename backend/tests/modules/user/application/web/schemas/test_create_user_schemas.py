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
                "logradouro": "Rua Teste",
                'numero': "564",
                "bairro": "Novo Teste",
                'cidade':'Joateste',
                'estado': "SP",
                'cep': '00000-000',
                "complemento": ""
            },
            'institution_id': "1cee6fe5-1fd5-4131-b054-4ec03358583a",
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
                            "logradouro": "Rua Teste",
                            'numero': "564",
                            "bairro": "Novo Teste",
                            'cidade':'Joateste',
                            "complemento": "",
                            'estado': "SP",
                            'cep': '00000-000'
                        },
                        'institution_id': "1cee6fe5-1fd5-4131-b054-4ec03358583a",
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
                            "logradouro": "Rua Teste",
                            'numero': "564",
                            "bairro": "Novo Teste",
                            'cidade':'Joateste',
                            "complemento": "",
                            'estado': "SP",
                            'cep': '00000-000'
                        },
                        'institution_id': "1cee6fe5-1fd5-4131-b054-4ec03358583a",
                        'password': '!Teste123@#$',
                        'role': 'hospital'
                    }
            CreateUserRequestSchema(**request)

    def test_address_missing_missing(self):
        with pytest.raises(MissingParameters):
            request = {
                        'name': "Pedro",
                        "phone": "+5511999999999",
                        'institution_id': "1cee6fe5-1fd5-4131-b054-4ec03358583a",
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
                    "logradouro": "Rua Teste",
                    'numero': "564",
                    "bairro": "Novo Teste",
                    'cidade':'Joateste',
                    'estado': "SP",
                    'cep': '00000-000',
                    "complemento": ""
                    },
                'institution_id': "1cee6fe5-1fd5-4131-b054-4ec03358583a",
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
                    "logradouro": "Rua Teste",
                    'numero': "564",
                    "bairro": "Novo Teste",
                    'cidade':'Joateste',
                    'estado': "SP",
                    'cep': '00000-000',
                    "complemento": ""
                    },
                'institution_id': "1cee6fe5-1fd5-4131-b054-4ec03358583a",
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
                    "logradouro": "Rua Teste",
                    'numero': "564",
                    "bairro": "Novo Teste",
                    'cidade':'Joateste',
                    'estado': "SP",
                    'cep': '00000-000',
                    "complemento": ""
                    },
                'institution_id': "1cee6fe5-1fd5-4131-b054-4ec03358583a",
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
                    "logradouro": "Rua Teste",
                    'numero': "564",
                    "bairro": "Novo Teste",
                    'cidade':'Joateste',
                    'estado': "SP",
                    'cep': '00000-000',
                    "complemento": ""
                    },
                'institution_id': "1cee6fe5-1fd5-4131-b054-4ec03358583a",
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
                'institution_id': "1cee6fe5-1fd5-4131-b054-4ec03358583a",
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
                    "logradouro": "Rua Teste",
                    'numero': "564",
                    "bairro": "Novo Teste",
                    'cidade':'Joateste',
                    'estado': "SP",
                    'cep': '00000-000',
                    "complemento": ""
                    },
                'institution_id': "1cee6fe5-1fd5-4131-b054-4ec03358583a",
                'password': '!Teste123@#$',
                'role': 'felipe'
                }
                
            create_user_request_schema = CreateUserRequestSchema(**request)

    def test_institution_id_type_invalid(self):
        with pytest.raises(WrongTypeParameter):
            request = {
                "name": "Pedro",
                "email": "pedro@aacd.com",
                "phone": "+5511999999999",
                "address": {
                    "logradouro": "Rua Teste",
                    'numero': "564",
                    "bairro": "Novo Teste",
                    'cidade': 'Joateste',
                    'estado': "SP",
                    'cep': '00000-000',
                    "complemento": ""
                },
                'institution_id': 123,
                'password': '!Teste123@#$',
                'role': 'hospital'
            }
            
            CreateUserRequestSchema(**request)
