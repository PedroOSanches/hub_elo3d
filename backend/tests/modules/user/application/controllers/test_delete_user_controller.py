from src.modules.user.application.controllers.delete_user_controller import DeleteUserController
from src.modules.user.infra.repositories.user_repository_mock import UserRepositoryMock
from src.modules.user.application.usecases.delete_user_usecase import DeleteUserUsecase
from uuid import UUID


class Test_DeleteUserController


    def test_delete_user(self):
        repo = UserRepositoryMock()
        usecase = DeleteUserUsecase(repo)

        controller = DeleteUserController(usecase)('0334c795-5e71-4c1e-8a0e-ab21a4fcdecf')

        assert controller != repo.users[0]
