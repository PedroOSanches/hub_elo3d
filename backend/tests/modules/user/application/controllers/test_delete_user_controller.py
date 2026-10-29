from src.modules.user.application.controllers.delete_user_controller import DeleteUserController
from src.modules.user.infra.repositories.user_repository_mock import UserRepositoryMock
from src.modules.user.application.usecases.delete_user_usecase import DeleteUserUsecase
from src.modules.user.application.web.schemas.delete_user_schema import DeleteUserRequestSchema
from uuid import UUID


class Test_DeleteUserController:


    def test_delete_user(self):
        repo = UserRepositoryMock()
        usecase = DeleteUserUsecase(repo)

        controller = DeleteUserController(usecase)(DeleteUserRequestSchema(id='b189d11a-25d1-430e-b5a1-c53db528337e'))

        assert controller != repo.users[0]
