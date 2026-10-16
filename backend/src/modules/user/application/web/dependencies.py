from src.modules.user.domain.repositories.user_repository_interface import IUserRepository
from src.modules.user.infra.repositories.user_repository_mock import UserRepositoryMock
from src.shared.environments import Environments, STAGE


def get_repo_user() -> IUserRepository:
    if Environments.get_envs().stage == STAGE.TEST.value:
        return UserRepositoryMock()
    else:
        return UserRepositoryMock()