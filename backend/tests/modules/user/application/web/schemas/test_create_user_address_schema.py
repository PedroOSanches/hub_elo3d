import pytest
from src.modules.user.application.web.schemas.create_user_schema import CreateUserAddressSchema, MissingParameters, WrongTypeParameter

class Test_CreateUserAddressSchema:

    def test_logradouro_missing(self):
            with pytest.raises(MissingParameters):
                request = {
                    'numero': "564",
                    "bairro": "Novo Teste",
                    'cidade':'Joateste',
                    "complemento": "",
                    'estado': "SP",                       
                    'cep': '00000-000'
                    }
                
                request = CreateUserAddressSchema(**request)
    
    def test_numero_missing(self):
        with pytest.raises(MissingParameters):
            request = {
                        'logradouro': "Rua teste",
                        "bairro": "Novo Teste",
                        'cidade':'Joateste',
                        "complemento": "",
                        'estado': "SP",
                        'cep': '00000-000',
                    }
            
            request = CreateUserAddressSchema(**request)
    
    def test_bairro_missing(self):
        with pytest.raises(MissingParameters):
            request = {
                'logradouro': "Rua teste",
                'numero': "564",
                'cidade':'Joateste',
                "complemento": "",
                'estado': "SP",
                'cep': '00000-000',
                }
    
            request = CreateUserAddressSchema(**request)
    
    
    def test_cidade_missing(self):
        with pytest.raises(MissingParameters):
            request = {
                'logradouro': "Rua teste",
                'numero': "564",
                "bairro": "Novo Teste",
                "complemento": "",
                'estado': "SP",
                'cep': '00000-000',
            }
            request = CreateUserAddressSchema(**request)
    
    def test_estado_missing(self):
        with pytest.raises(MissingParameters):
            request = {
                'logradouro': "Rua teste",
                'numero': "564",
                "bairro": "Novo Teste",
                'cidade':'Joateste',
                "complemento": "",
                'cep': '00000-000',
                }

            request = CreateUserAddressSchema(**request)
        
    def test_cep_missing(self):
        with pytest.raises(MissingParameters):
            request = {
                'logradouro': "Rua teste",
                'numero': "564",
                "bairro": "Novo Teste",
                'cidade':'Joateste',
                "complemento": "",
                "estado": "SP",
                }
            
            request = CreateUserAddressSchema(**request)

    def test_logradouro_type_invalid(self):

        with pytest.raises(WrongTypeParameter):
            request = {
                "logradouro": {"Rua": "Teste"},
                'numero': "564",
                "bairro": "Novo Teste",
                'cidade':'Joateste',
                'estado': "SP",
                'cep': '00000-000',
                "complemento": ""
                }
            create_user_address_schema = CreateUserAddressSchema(**request)

    def test_numero_type_invalid(self):
        with pytest.raises(WrongTypeParameter):
            request = {
                "logradouro": "Rua Teste",
                'numero': 564,
                "bairro": "Novo Teste",
                'cidade':'Joateste',
                'estado': "SP",
                'cep': '00000-000',
                "complemento": ""
                }
                
            create_user_address_schema = CreateUserAddressSchema(**request)

    def test_bairro_type_invalid(self):
        with pytest.raises(WrongTypeParameter):
            request = {
                "logradouro": "Rua Teste",
                'numero': "564",
                "bairro": 3,
                'cidade':'Joateste',
                'estado': "SP",
                'cep': '00000-000',
                "complemento": ""
                }
                
            create_user_address_schema = CreateUserAddressSchema(**request)

    def test_cidade_type_invalid(self):

        with pytest.raises(WrongTypeParameter):
            request = {
                "logradouro": "Rua Teste",
                'numero': "564",
                "bairro": "Novo Teste",
                'cidade': 53,
                'estado': "SP",
                'cep': '00000-000',
                "complemento": ""
                }
                
            create_user_address_schema = CreateUserAddressSchema(**request)

    def test_estado_type_invalid(self):
        with pytest.raises(WrongTypeParameter):
            request = {
                "logradouro": "Rua Teste",
                'numero': "564",
                "bairro": "Novo Teste",
                'cidade':'Joateste',
                'estado': 65,
                'cep': '00000-000',
                "complemento": ""
                }
                
            create_user_address_schema = CreateUserAddressSchema(**request)

    def test_cep_type_invalid(self):
        with pytest.raises(WrongTypeParameter):
            request = {
                "logradouro": "Rua Teste",
                'numero': "564",
                "bairro": "Novo Teste",
                'cidade': 'Joateste',
                'estado': "SP",
                'cep': 0,
                "complemento": ""
            }
                
            create_user_address_schema = CreateUserAddressSchema(**request)

    def test_complemento_type_invalid(self):
        with pytest.raises(WrongTypeParameter):
            request = {
                "logradouro": "Rua Teste",
                'numero': "564",
                "bairro": "Novo Teste",
                'cidade':'Joateste',
                'estado': "SP",
                'cep': '00000-000',
                "complemento": [0, 1, 0, 0]
                }
            create_user_address_schema = CreateUserAddressSchema(**request)