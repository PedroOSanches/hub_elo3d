from src.modules.user.domain.repositories.user_repository_interface import IUserRepository
from src.shared.environments.environments import env


def get_repo_user() -> IUserRepository:
    return env.repo_user