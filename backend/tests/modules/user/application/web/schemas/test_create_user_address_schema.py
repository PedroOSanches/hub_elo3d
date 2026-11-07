import pytest
from src.modules.user.application.web.schemas.create_user_schema import CreateUserAddressSchema, MissingParameters, WrongTypeParameter

class Test_CreateUserAddressSchema:

    def test_street_missing(self):
            with pytest.raises(MissingParameters):
                request = {
                    'number': "564",
                    "neighborhood": "Novo Teste",
                    'city':'Joateste',
                    "address_details": "",
                    'state': "SP",                       
                    'cep': '00000-000'
                    }
                
                request = CreateUserAddressSchema(**request)
    
    def test_number_missing(self):
        with pytest.raises(MissingParameters):
            request = {
                        'street': "Rua teste",
                        "neighborhood": "Novo Teste",
                        'city':'Joateste',
                        "address_details": "",
                        'state': "SP",
                        'cep': '00000-000',
                    }
            
            request = CreateUserAddressSchema(**request)
    
    def test_neighborhood_missing(self):
        with pytest.raises(MissingParameters):
            request = {
                'street': "Rua teste",
                'number': "564",
                'city':'Joateste',
                "address_details": "",
                'state': "SP",
                'cep': '00000-000',
                }
    
            request = CreateUserAddressSchema(**request)
    
    
    def test_city_missing(self):
        with pytest.raises(MissingParameters):
            request = {
                'street': "Rua teste",
                'number': "564",
                "neighborhood": "Novo Teste",
                "address_details": "",
                'state': "SP",
                'cep': '00000-000',
            }
            request = CreateUserAddressSchema(**request)
    
    def test_state_missing(self):
        with pytest.raises(MissingParameters):
            request = {
                'street': "Rua teste",
                'number': "564",
                "neighborhood": "Novo Teste",
                'city':'Joateste',
                "address_details": "",
                'cep': '00000-000',
                }

            request = CreateUserAddressSchema(**request)
        
    def test_cep_missing(self):
        with pytest.raises(MissingParameters):
            request = {
                'street': "Rua teste",
                'number': "564",
                "neighborhood": "Novo Teste",
                'city':'Joateste',
                "address_details": "",
                "state": "SP",
                }
            
            request = CreateUserAddressSchema(**request)

    def test_street_type_invalid(self):

        with pytest.raises(WrongTypeParameter):
            request = {
                "street": {"Rua": "Teste"},
                'number': "564",
                "neighborhood": "Novo Teste",
                'city':'Joateste',
                'state': "SP",
                'cep': '00000-000',
                "address_details": ""
                }
            create_user_address_schema = CreateUserAddressSchema(**request)

    def test_number_type_invalid(self):
        with pytest.raises(WrongTypeParameter):
            request = {
                "street": "Rua Teste",
                'number': 564,
                "neighborhood": "Novo Teste",
                'city':'Joateste',
                'state': "SP",
                'cep': '00000-000',
                "address_details": ""
                }
                
            create_user_address_schema = CreateUserAddressSchema(**request)

    def test_neighborhood_type_invalid(self):
        with pytest.raises(WrongTypeParameter):
            request = {
                "street": "Rua Teste",
                'number': "564",
                "neighborhood": 3,
                'city':'Joateste',
                'state': "SP",
                'cep': '00000-000',
                "address_details": ""
                }
                
            create_user_address_schema = CreateUserAddressSchema(**request)

    def test_city_type_invalid(self):

        with pytest.raises(WrongTypeParameter):
            request = {
                "street": "Rua Teste",
                'number': "564",
                "neighborhood": "Novo Teste",
                'city': 53,
                'state': "SP",
                'cep': '00000-000',
                "address_details": ""
                }
                
            create_user_address_schema = CreateUserAddressSchema(**request)

    def test_state_type_invalid(self):
        with pytest.raises(WrongTypeParameter):
            request = {
                "street": "Rua Teste",
                'number': "564",
                "neighborhood": "Novo Teste",
                'city':'Joateste',
                'state': 65,
                'cep': '00000-000',
                "address_details": ""
                }
                
            create_user_address_schema = CreateUserAddressSchema(**request)

    def test_cep_type_invalid(self):
        with pytest.raises(WrongTypeParameter):
            request = {
                "street": "Rua Teste",
                'number': "564",
                "neighborhood": "Novo Teste",
                'city': 'Joateste',
                'state': "SP",
                'cep': 0,
                "address_details": ""
            }
                
            create_user_address_schema = CreateUserAddressSchema(**request)

    def test_address_details_type_invalid(self):
        with pytest.raises(WrongTypeParameter):
            request = {
                "street": "Rua Teste",
                'number': "564",
                "neighborhood": "Novo Teste",
                'city':'Joateste',
                'state': "SP",
                'cep': '00000-000',
                "address_details": [0, 1, 0, 0]
                }
            create_user_address_schema = CreateUserAddressSchema(**request)