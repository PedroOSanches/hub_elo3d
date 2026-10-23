from uuid import uuid4

import pytest

from src.modules.printers.domain.entities.printer import Printer
from src.modules.printers.domain.errors.printer_errors import PrinterNotFoundError
from src.modules.printers.infra.repositories.printer_repository_mock import (
    PrinterRepositoryMock,
)


def make_printer(usuario_id=None, apelido="AD5X 1") -> Printer:
    return Printer(
        apelido=apelido,
        modelo="Flashforge AD5X",
        tecnologia_impressao="FDM",
        usuario_id=usuario_id or uuid4(),
    )


class TestPrinterRepositoryMock:
    def setup_method(self):
        self.repo = PrinterRepositoryMock()

    def test_create_and_get_printer(self):
        printer = make_printer()

        self.repo.create_printer(printer)

        assert self.repo.get_printer(printer.id) == printer

    def test_get_printer_not_found(self):
        with pytest.raises(PrinterNotFoundError):
            self.repo.get_printer(uuid4())

    def test_get_all_printers_empty(self):
        assert self.repo.get_all_printers() == []

    def test_get_all_printers(self):
        self.repo.create_printer(make_printer())
        self.repo.create_printer(make_printer())

        assert len(self.repo.get_all_printers()) == 2

    def test_get_all_printers_filtered_by_user(self):
        user_id = uuid4()
        mine = make_printer(usuario_id=user_id)
        self.repo.create_printer(mine)
        self.repo.create_printer(make_printer())

        result = self.repo.get_all_printers(user_id)

        assert result == [mine]

    def test_update_printer(self):
        printer = make_printer()
        self.repo.create_printer(printer)
        updated = printer.model_copy(update={"apelido": "Nova"})

        self.repo.update_printer(printer.id, updated)

        assert self.repo.get_printer(printer.id).apelido == "Nova"

    def test_update_printer_not_found(self):
        printer = make_printer()

        with pytest.raises(PrinterNotFoundError):
            self.repo.update_printer(printer.id, printer)

    def test_delete_printer(self):
        printer = make_printer()
        self.repo.create_printer(printer)

        self.repo.delete_printer(printer.id)

        with pytest.raises(PrinterNotFoundError):
            self.repo.get_printer(printer.id)

    def test_delete_printer_not_found(self):
        with pytest.raises(PrinterNotFoundError):
            self.repo.delete_printer(uuid4())