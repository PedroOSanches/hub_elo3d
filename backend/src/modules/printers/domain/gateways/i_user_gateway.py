import abc
from abc import abstractmethod
from uuid import UUID


class IUserGateway(abc.ABC):
    #reconhece o modulo user

    @abstractmethod
    def exists(self, user_id: UUID) -> bool:
        #se tiver um usuario com esse ID retorna true, se não retorna false
        pass