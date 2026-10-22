from src.modules.user.application.controllers.get_all_users_controller import GetAllUsersController
from src.modules.user.application.usecases.get_all_users_usecase import GetAllUsersUsecase
from src.modules.user.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_GetAllUserController:


    def test_get_all_user_controller(self):
        repo = UserRepositoryMock()
        usecase = GetAllUsersUsecase(repo)
        controller = GetAllUsersController(usecase)

        assert controller()[0]['name'] == 'User'