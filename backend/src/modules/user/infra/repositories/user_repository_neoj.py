from neo4j import  GraphDatabase

from src.modules.user.domain.entities.user import User
from src.modules.user.domain.repositories.user_repository_interface import IUserRepository
from src.shared.environments.environments import env
from neo4j import Session


class UserRepositoyNeoJ(IUserRepository):

    def __init__(self, connection: Session) -> None:
        self.connection = connection

    def create_user(self, user: User) -> User:

        result = self.connection.run(
            """CREATE(u:User {user_id: $user_id, name: $name, email: $email})"""
        )