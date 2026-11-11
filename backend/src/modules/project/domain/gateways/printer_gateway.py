from abc import ABC, abstractmethod
from uuid import UUID

class IPrinterGateway(ABC):
    @abstractmethod
    def exists(self, printer_id: UUID) -> bool:
        pass