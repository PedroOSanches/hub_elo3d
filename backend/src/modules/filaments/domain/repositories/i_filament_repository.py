import abc
from abc import abstractmethod
from uuid import UUID

from src.modules.filaments.domain.entities.filament import Filament


class IFilamentRepository(abc.ABC):
    @abstractmethod
    def get_filament(self, filament_id: UUID) -> Filament:
    
        pass

    @abstractmethod
    def get_all_filaments(self) -> list[Filament]:
    
        pass