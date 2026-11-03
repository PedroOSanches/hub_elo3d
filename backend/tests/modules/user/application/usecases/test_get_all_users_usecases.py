from src.modules.user.application.usecases.get_all_users_usecase import GetAllUsersUsecase
from src.modules.user.infra.repositories.user_repository_mock import UserRepositoryMock

class Test_GetAllUserUsecase:

    def test_get_all_user_usecase(self):

        repo = UserRepositoryMock()

        usecase = GetAllUsersUsecase(repo)()


        assert repo.users[0] == usecase[0]