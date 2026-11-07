from src.modules.user.domain.repositories.user_repository_interface import IUserRepository
from src.modules.user.infra.repositories.user_repository_mock import UserRepositoryMock
from src.shared.environments.environments import Environments, STAGE, env


def get_repo_user() -> IUserRepository:
    return env.repo_user