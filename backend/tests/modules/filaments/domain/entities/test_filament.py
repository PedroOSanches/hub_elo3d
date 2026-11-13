from uuid import uuid4

import pytest
from pydantic import ValidationError

from src.modules.filaments.domain.entities.filament import Filament


class TestFilament:
    def test_create_filament(self):
        filament = Filament(nome="PLA Branco", tipo="PLA")

        assert filament.nome == "PLA Branco"
        assert filament.tipo == "PLA"

    def test_each_filament_gets_its_own_id(self):
        assert Filament(nome="A", tipo="PLA").id != Filament(nome="A", tipo="PLA").id

    def test_use_given_id(self):
        filament_id = uuid4()

        assert Filament(id=filament_id, nome="A", tipo="PLA").id == filament_id

    def test_strip_whitespace(self):
        assert Filament(nome="  PLA  ", tipo=" PLA ").nome == "PLA"

    def test_empty_nome_is_invalid(self):
        with pytest.raises(ValidationError):
            Filament(nome="", tipo="PLA")

    def test_empty_tipo_is_invalid(self):
        with pytest.raises(ValidationError):
            Filament(nome="PLA", tipo="")