from uuid import UUID
from src.modules.user.domain.entities.user import User
from src.modules.user.domain.repositories.user_repository_interface import IUserRepository


class DeleteUserUsecase:

    def __init__(self, repo: IUserRepository) -> None:
        self.repo = repo

    def __call__(self, id: UUID) -> User:

        return self.repo.delete_user(id)