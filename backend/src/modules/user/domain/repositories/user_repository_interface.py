import abc
from abc import abstractmethod


from ..entities.user import User

class IUserRepository(abc.ABC):
    @abstractmethod
    def get_user(self, id: str) -> User:
        """
        Retorna um objeto "User" a partir do seu ID

        Em caso não encontrado retorna NoUsersFound
        """

        pass

    @abstractmethod
    def get_all_users(self) -> list[User]:
        """
        Retorna todos os usuários


        Em caso de nenhum usuário encontrado retorna NoUsersFound
        """
        pass

    @abstractmethod
    def create_user(self, user: User) -> User:
        """
        Cria um novo usuário

        Em caso de sucesso retorna o usuario criado

        Caso encontre um usuário já existente com as mesmas credencias retorna DuplicatedUser
        """
        pass

    @abstractmethod
    def update_user(
            self, 
            id: str, 
            updated_user: User
            ) -> User:
        """
        Atualiza os campos de um usuário de acordo com o id

        Retorna o usuário com os campos atualizados


        Em caso de haver mais de um usuário registrado retorna DuplicatedUser
        Em caso de não encontre nenhum usuario retorna NoUsersFound
        """

        pass
    
    @abstractmethod
    def delete_user(self, id: str) -> dict:
        """
        Deleta um usuário retorna
        ```
        {
            status: "ok"
        }
        ```
        """
        pass