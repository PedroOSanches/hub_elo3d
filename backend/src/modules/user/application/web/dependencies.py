from src.modules.user.domain.repositories.user_repository_interface import (
    IUserRepository,
)
from src.modules.user.infra.repositories.user_repository_mock import UserRepositoryMock
from src.modules.user.infra.repositories.user_repository_neoj import UserRepositoyNeoJ
from src.shared.environments.environments import env
from src.shared.environments.neo4j_connection_factory import connection

_repository_mock = UserRepositoryMock()


def get_repo_user() -> IUserRepository:
    if env.stage.value == "PROD":
        return UserRepositoyNeoJ(connection=connection)
    else:
        return _repository_mock