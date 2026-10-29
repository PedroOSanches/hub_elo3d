from abc import abstractmethod, ABC
from src.modules.auth.domain.entities.auth_user import AuthUser
from uuid import UUID
class IGatewayUser(ABC):

    @classmethod
    @abstractmethod
    def get_repo_user(cls):
        """
        Recebe o repositorio de usuario
        """

    @abstractmethod
    def get_user_by_email(self, email: str) -> AuthUser:
        """
        Busca o usuario por meio do email\n
        Se não encontrado retorna NoUsersFound
        
        """

    @abstractmethod
    def get_user_by_id(self, user_id: UUID) -> AuthUser:
        """
        Busca usuario por meio do id do usuário\n
        Se não encontrado retorna NoUsersFound
        """