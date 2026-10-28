from abc import ABC, abstractmethod



class IResponse(ABC):

    @property
    @abstractmethod
    def status_code(self) -> int:
        pass

    @property
    @abstractmethod
    def data(self) -> dict:
        pass
