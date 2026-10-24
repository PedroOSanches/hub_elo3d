from uuid import UUID
from src.modules.user.domain.repositories.user_repository_interface import IUserRepository


class DeleteUserUsecase:

    def __init__(self, repo: IUserRepository):
        self.repo = repo

    def __call__(self, id: UUID):

        return self.repo.delete_user(id)