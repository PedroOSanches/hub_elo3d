from uuid import uuid4

import pytest
from pydantic import ValidationError

from src.modules.filaments.domain.entities.filament import Filament


class TestFilament:
    def test_create_filament(self):
        filament = Filament(
            tipo="PLA"
            )

        assert filament.tipo == "PLA"

    def test_each_filament_gets_its_own_id(self):
        assert Filament(tipo="PLA").filament_id != Filament(tipo="PLA").filament_id

    def test_use_given_id(self):
        filament_id = uuid4()

        assert Filament(filament_id=filament_id, tipo="PLA").filament_id == filament_id

    def test_strip_whitespace(self):
        assert Filament(tipo=" PLA ").tipo == "PLA"

    def test_empty_tipo_is_invalid(self):
        with pytest.raises(ValidationError):
            Filament(tipo="")