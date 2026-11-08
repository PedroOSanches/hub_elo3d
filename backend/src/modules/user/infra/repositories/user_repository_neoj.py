from uuid import UUID

from neo4j.exceptions import ConstraintError
from neo4j import Session

from src.modules.user.domain.entities.user import User
from src.modules.user.infra.dto.user_dto import UserDTO
from src.modules.user.domain.repositories.user_repository_interface import IUserRepository
from src.modules.user.domain.errors.user_usecase_errors import NoUsersFound, DuplicatedUser
from src.shared.environments.neo4j_connection_factory import Neo4JConnectionFactory
from src.shared.errors.database_error import DatabaseError
from src.shared.environments.environments import env


class UserRepositoyNeoJ(IUserRepository):

    def __init__(self, connection: Neo4JConnectionFactory) -> None:
        self.connection = connection

    def create_user(self, user: User) -> User:

        query = """
            CREATE (u:User)
            SET u = $user

            CREATE (a:Address)
            SET a = $address

            CREATE (u)-[:HAS_ADDRESS]->(a)

            RETURN u AS user, a AS address;
            """
        try:
            u, a = UserDTO.entitie_to_dict(user)


            result = self.connection.execute_write(
                lambda tx: tx.run(
                    query,
                    user=u,
                    address=a
                ).single()
            )

            if result is None:
                raise DatabaseError()
        except ConstraintError as err:

            if 'user_id_unique' in err.message:
                raise DuplicatedUser('user_id')
            if "user_email_is_unique" in err.message:
                raise DuplicatedUser('email')

            raise DatabaseError()
        
        return UserDTO.dict_to_entitie(result.data())

    def get_user(self, user_id: UUID) -> User:
        query = """
            MATCH(u:User {user_id: $user_id})
            OPTIONAL MATCH (u)-[:HAS_ADDRESS]->(a:Address)

            RETURN u AS user, a AS address;
            """
        try:

            result = self.connection.execute_read(
                lambda tx: tx.run(
                    query=query,
                    user_id=str(user_id)
                ).single()
            )

            if result is None:
                raise NoUsersFound('id')
        except NoUsersFound:
            raise
        except Exception:
            raise DatabaseError()
            
        return UserDTO.dict_to_entitie(result.data())

    def get_all_users(self) -> list[User]:
        query = """
                MATCH (u: User)-[:HAS_ADDRESS]->(a)
                RETURN u AS user, a AS address;
                """
        try:
            result = self.connection.execute_read(
                lambda tx:[
                    UserDTO.dict_to_entitie(record.data())
                    for record in tx.run(query)
                    ]
            )

            if not result:
                raise NoUsersFound('this query')

            return result
        except NoUsersFound:
            raise
        except Exception:
            raise DatabaseError()

    def get_user_by_email(self, email: str) -> User:
        query = """
        MATCH (u:User {email: $email})-[:HAS_ADDRESS]->(a:Address)
        RETURN u AS user, a AS address;
        """

        try:
            result = self.connection.execute_read(
                lambda tx: tx.run(
                    query=query,
                    email=str(email)
                ).single()
            )

            if result is None:
                raise NoUsersFound('email')

        
        except NoUsersFound:
            raise
        except Exception:
            raise DatabaseError()
        
        return UserDTO.dict_to_entitie(result.data())

    def update_user(self, updated_user: User) -> User:
        query = """
            MATCH (u:User {user_id: $user_id})-[:HAS_ADDRESS]->(a)
            SET u = $user
            SET a = $address

            return u AS user, a AS address;
        """

        try:
            u, a = UserDTO.entitie_to_dict(updated_user)
            result = self.connection.execute_write(
                lambda tx: tx.run(
                    query=query,
                    user_id=str(updated_user.user_id),
                    user = u,
                    address = a
                    
                ).single()
            )

            if result is None:
                raise NoUsersFound('user_id')
        except NoUsersFound:
            raise
        except Exception:
            raise DatabaseError()


        return UserDTO.dict_to_entitie(result.data())

    def delete_user(self, user_id: UUID) -> User:
        query = """
            MATCH (u:User {user_id: $user_id})
            OPTIONAL MATCH (u)-[:HAS_ADDRESS]->(a:Address)

            WITH
                properties(u) AS user,
                properties(a) AS address,
                u,
                a

            DETACH DELETE u, a

            RETURN user, address
        """
        
        try:
            result = self.connection.execute_write(
                lambda tx: tx.run(
                    query=query,
                    user_id=str(user_id),
        
                ).single()
            )

            if result is None:
                raise NoUsersFound('user_id')
        except NoUsersFound:
            raise
        except:
            raise DatabaseError()


        return UserDTO.dict_to_entitie(result.data())