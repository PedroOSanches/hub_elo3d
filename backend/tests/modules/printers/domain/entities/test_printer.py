from uuid import uuid4

import pytest
from pydantic import ValidationError

from src.modules.printers.domain.entities.printer import Printer
from src.modules.printers.domain.entities.status_printer import StatusPrinter


def make_printer(**kwargs) -> Printer:
    data = {
        "apelido": "AD5X 1",
        "modelo": "Flashforge AD5X",
        "tecnologia_impressao": "FDM",
        "usuario_id": uuid4(),
    }
    data.update(kwargs)
    return Printer(**data)


class TestPrinter:
    def test_create_printer_with_defaults(self):
        printer = make_printer()

        assert printer.status == StatusPrinter.DISPONIVEL
        assert printer.filamentos_aceitos == []
        assert printer.disponivel is True

    def test_each_printer_gets_its_own_id(self):
        assert make_printer().id != make_printer().id

    def test_strip_whitespace_from_text_fields(self):
        printer = make_printer(apelido="  AD5X 1  ")

        assert printer.apelido == "AD5X 1"

    def test_remove_duplicated_filaments(self):
        filamento = uuid4()

        printer = make_printer(filamentos_aceitos=[filamento, filamento])

        assert printer.filamentos_aceitos == [filamento]

    def test_empty_apelido_is_invalid(self):
        with pytest.raises(ValidationError):
            make_printer(apelido="")

    def test_invalid_usuario_id_is_invalid(self):
        with pytest.raises(ValidationError):
            make_printer(usuario_id="not-a-uuid")

    def test_change_status(self):
        printer = make_printer()

        printer.alterar_status(StatusPrinter.EM_USO)

        assert printer.status == StatusPrinter.EM_USO
        assert printer.disponivel is False