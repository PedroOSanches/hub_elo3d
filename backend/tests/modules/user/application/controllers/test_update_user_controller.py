import pytest

from src.modules.user.application.controllers.update_user_controller import (
    UpdateUserController, 
    UpdateUserUsecase, 
    UpdateUserRequestSchema
)

from src.shared.errors.controller_error import WrongTypeParameter
from src.modules.user.infra.repositories.user_repository_mock import UserRepositoryMock, NoUsersFound


class Test_UpdateUserController:

    def test_update_user_controller(self):
        repo = UserRepositoryMock()
        usecase = UpdateUserUsecase(
            repo=repo
        )

        controller = UpdateUserController(
            usecase=usecase
        )

        request = {
            'id': 'b189d11a-25d1-430e-b5a1-c53db528337e',
            'new_name': 'Angela'
        }


        controller(UpdateUserRequestSchema(**request))

        assert repo.users[0].name == 'Angela'

    def test_update_user_type_parameter_invalid(self):
        repo = UserRepositoryMock()
        usecase = UpdateUserUsecase(
            repo=repo
        )
        
        controller = UpdateUserController(
            usecase=usecase
        )

        request = {
            'id': 'b189d11a-25d1-430e-b5a1-c53db528337e',
            'new_name': 2
        }
        
        with pytest.raises(WrongTypeParameter):
            controller(UpdateUserRequestSchema(**request))

    

    def test_update_user_address(self):
        repo = UserRepositoryMock()
        usecase = UpdateUserUsecase(
            repo=repo
        )
        
        controller = UpdateUserController(
            usecase=usecase
        )
        
        request = {
            'id': 'b189d11a-25d1-430e-b5a1-c53db528337e',
            'address': {
                'new_logradouro': 'Av. Bernadino Carvalho Pinto'
            }
        }
        
        
        controller(UpdateUserRequestSchema(**request))
        
        assert repo.users[0].address.logradouro == request['address']['new_logradouro']

    def test_update_user_type_parameter_invalid(self):
            repo = UserRepositoryMock()
            usecase = UpdateUserUsecase(
                repo=repo
            )
            
            controller = UpdateUserController(
                usecase=usecase
            )
    
            request = {
                'id': 'b189d11a-25d1-430e-b5a1-c53db528337e',
                'address': {
                    'new_logradouro': [0, 123]
                }
            }
            
            with pytest.raises(WrongTypeParameter):
                controller(UpdateUserRequestSchema(**request))

    def test_update_user_not_found(self):
        repo = UserRepositoryMock()
        usecase = UpdateUserUsecase(
            repo=repo
        )
        
        controller = UpdateUserController(
            usecase=usecase
        )

        request = {
            'id': 'b189d12a-25d1-430e-b5a1-c53db528337e',
            'new_name': 'BrenoORossini'
        }
        
        with pytest.raises(NoUsersFound):
            controller(UpdateUserRequestSchema(**request))
