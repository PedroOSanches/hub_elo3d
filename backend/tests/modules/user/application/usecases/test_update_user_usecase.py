import pytest
from uuid import UUID
from src.modules.user.application.usecases.update_user_usecase import UpdateUserUsecase
from src.modules.user.domain.errors.user_usecase_errors import NoUsersFound
from src.modules.user.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_UpdateUserUsecase:


    def test_update_user_usecase(self):
        repo = UserRepositoryMock()
        usecase = UpdateUserUsecase(repo=repo)(
            user_id=UUID('b189d11a-25d1-430e-b5a1-c53db528337e'),
            new_name='Giulia',
            new_address=None,
            new_phone=None,
            new_password=None
        )

        assert repo.users[0].name == 'Giulia'

        def test_update_user_usecase(self):
            repo = UserRepositoryMock()
            with pytest.raises(NoUsersFound):
                usecase = UpdateUserUsecase(repo=repo)(
                    user_id=UUID('b189d11a-25d1-430e-b5a1-c53db528337e'),
                    new_name='Giulia',
                    new_address=None,
                    new_phone=None,
                    new_password=None
                )