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
                'cidade': 'São Paulo',
                'estado': "SP",
                'cep': '00000-000'
            },
            'password': '!Teste123@#$',
            'role': 'hospital'
        }

        user = controller(request=CreateUserRequestSchema(**request))

        assert user.name == "Pedro"