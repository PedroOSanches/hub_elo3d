from src.modules.user.application.controllers.get_user_controller import GetUserController, GetUserUsecase

from src.modules.user.application.usecases.get_user_usecase import GetUserUsecase
from src.modules.user.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_GetUserController:

    def test_get_user_controller(self):

        usecase = GetUserUsecase(UserRepositoryMock())
        controller = GetUserController(usecase)

