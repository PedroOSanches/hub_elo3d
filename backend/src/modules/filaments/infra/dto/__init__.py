from typing import Any

from src.modules.filaments.domain.entities.filament import Filament


class FilamentDTO:

    def from_entitie_to_dict(self, filament: Filament) -> dict:

        return filament.model_dump(mode='python')

    def from_dict_to_entitie(self, filament_dict: dict[str, Any]) -> Filament:
        return Filament(**filament_dict)