from uuid import UUID

from src.modules.user.application.usecases.delete_user_usecase import DeleteUserUsecase
from src.modules.user.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_DeleteUserUsecase:

    def test_delete_user_usercase(self):
        repo = UserRepositoryMock()
        usecase = DeleteUserUsecase(repo)

        user = usecase(id=UUID('0334c795-5e71-4c1e-8a0e-ab21a4fcdecf'))

        assert repo.users[0] != user