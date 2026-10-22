from typing import Any
from uuid import UUID
from src.modules.user.domain.repositories.user_repository_interface import IUserRepository, User


class GetAllUsersUsecase:

    def __init__(self, repo: IUserRepository) -> None:
        self.repo = repo

    def __call__(self) -> list[User]:

        return self.repo.get_all_users()