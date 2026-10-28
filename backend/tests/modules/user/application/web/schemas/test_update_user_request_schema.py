import pytest
from src.modules.user.application.web.schemas.update_user_request_schema import UpdateUserRequestSchema, UpdateAddressRequestSchema, WrongTypeParameter, MissingParameters


class Test_UpdateUserRequestSchema:

    def test_update_user_request_schema_type_invalid(self):

        request = {
            'user_id': 'b189d11a-25d1-430e-b5a1-c53db528337e',
            'new_name': ['Rafael']
        }

        with pytest.raises(WrongTypeParameter):
            user = UpdateUserRequestSchema(**request)
    
    def test_update_user_request_schema_missing_parameters(self):

        request = {
            'user_id': 'b189d11a-25d1-430e-b5a1-c53db528337e',
        }

        with pytest.raises(MissingParameters):
            user = UpdateUserRequestSchema(**request)


class Test_UpdateUserAddressRequestSchema:

    def test_update_user_address_request_schema_type_invalid(self):
        request = {
            'new_logradouro': 52
        }


        with pytest.raises(WrongTypeParameter):
            UpdateAddressRequestSchema(**request)
    
    def test_update_user_address_request_schema_missing_parameters(self):
        request = {
        }


        with pytest.raises(MissingParameters):
            UpdateAddressRequestSchema(**request)
