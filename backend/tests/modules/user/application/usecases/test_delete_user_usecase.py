from uuid import UUID

from src.modules.user.application.usecases.delete_user_usecase import DeleteUserUsecase
from src.modules.user.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_DeleteUserUsecase:

    def test_delete_user_usercase(self):
        repo = UserRepositoryMock()
        usecase = DeleteUserUsecase(repo)

        user = usecase(id=UUID('b189d11a-25d1-430e-b5a1-c53db528337e'))

        assert repo.users[0] != user