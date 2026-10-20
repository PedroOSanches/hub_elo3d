from typing import Any

from src.modules.user.domain.entities.user import User
from src.modules.user.domain.repositories.user_repository_interface import IUserRepository
from uuid import UUID

class GetUserUsecase:

    def __init__(self, repo: IUserRepository) -> None:
        self.repo = repo

    def __call__(self, id: UUID) -> User:
        return self.repo.get_user(id=id)