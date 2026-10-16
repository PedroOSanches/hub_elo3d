import pytest


from src.modules.user.application.controllers.create_user_controller import CreateUserController, CreateUserRequestSchema, CreateUserUsecase
from src.modules.user.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_CreateUserController():

    def test_create_user_controller(self):
        repo = UserRepositoryMock()
        usecase = CreateUserUsecase(repo)
        controller = CreateUserController(usecase)

        request = {
            "name": "Pedro",
            "email":"pedro@aacd.com",
            "phone":"+5511999999999",
            "address": {
                "logradouro": "Rua Teste",
                'numero': "564",
                "bairro": "Novo Teste",
                "complemento": "",
                'estado': "SP",
                'cep': '00000-000'
            },
            'institution_id': "1cee6fe5-1fd5-4131-b054-4ec03358583a",
            'password': 'teste123@#$'
        }

        user = controller(request=CreateUserRequestSchema(**request))

        assert user['name'] == "Pedro"