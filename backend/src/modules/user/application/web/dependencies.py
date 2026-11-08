from src.modules.user.infra.repositories.user_repository_mock import UserRepositoryMock
from src.modules.user.infra.repositories.user_repository_neoj import UserRepositoyNeoJ
from src.shared.environments.neo4j_connection_factory import Neo4JConnectionFactory
from src.modules.user.domain.repositories.user_repository_interface import IUserRepository
from src.shared.environments.environments import env

def get_connection():
    return Neo4JConnectionFactory()

def get_repo_user() -> IUserRepository:
    if env.stage != "TEST" or env.stage != "DOTENV":
        return UserRepositoyNeoJ(get_connection())
    else:
        return UserRepositoryMock()