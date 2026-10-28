from src.modules.user.domain.repositories.user_repository_interface import IUserRepository
from src.modules.user.domain.repositories.institution_repository_interface import IInstitutionRepository
from src.modules.user.infra.repositories.institution_repository_mock import InstitutionRepositoryMock
from src.modules.user.infra.repositories.user_repository_mock import UserRepositoryMock
from src.shared.environments import Environments, STAGE, env


def get_repo_user() -> IUserRepository:
    return env.repo_user

def get_repo_institution() -> IInstitutionRepository:
    if Environments.get_envs().stage == STAGE.TEST.value:
        return InstitutionRepositoryMock()
    else:
        return InstitutionRepositoryMock()