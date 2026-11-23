from uuid import uuid7

import pytest

from src.modules.printers.domain.entities.printer import Printer
from src.modules.printers.domain.entities.status_printer import StatusPrinter
from src.modules.printers.domain.errors.printer_errors import (
    PrinterNotFoundError,
    UserNotFoundError,
)
from src.modules.printers.infra.repositories.printer_repository_neo import (
    PrinterRepositoryNeo,
)
from src.shared.errors.database_error import DatabaseError


class FakeResult:
    def __init__(self, rows):
        self.rows = rows

    def single(self):
        return self.rows[0] if self.rows else None

    def __iter__(self):
        return iter(self.rows)


class FakeTx:
    def __init__(self, rows):
        self.rows = rows
        self.calls = []

    def run(self, query, **params):
        self.calls.append((query, params))
        return FakeResult(self.rows)


class FakeConnection:
    def __init__(self, rows=None, error=None):
        self.tx = FakeTx(rows or [])
        self.error = error

    def _run(self, callback):
        if self.error:
            raise self.error
        return callback(self.tx)

    execute_read = _run
    execute_write = _run


def make_printer(**kw) -> Printer:
    data = dict(
        apelido="Ender",
        modelo="Ender 3",
        tecnologia_impressao="FDM",
        usuario_id=uuid7(),
        filamentos_aceitos=[uuid7()],
    )
    data.update(kw)
    return Printer(**data)


def row(printer: Printer) -> dict:
    return {
        "printer": {
            "id": str(printer.id),
            "apelido": printer.apelido,
            "modelo": printer.modelo,
            "tecnologia_impressao": printer.tecnologia_impressao,
            "status": printer.status.value,
        },
        "user_id": str(printer.usuario_id),
        "filament_ids": [str(f) for f in printer.filamentos_aceitos],
    }


def test_create_does_not_store_relations_as_properties():
    conn = FakeConnection(rows=[{"printer": {}}])
    printer = make_printer()
    assert PrinterRepositoryNeo(conn).create_printer(printer) == printer
    params = conn.tx.calls[0][1]
    assert params["printer"]["id"] == str(printer.id)
    assert params["printer"]["status"] == "disponivel"
    assert "usuario_id" not in params["printer"]
    assert "filamentos_aceitos" not in params["printer"]
    assert params["user_id"] == str(printer.usuario_id)
    assert params["filament_ids"] == [str(printer.filamentos_aceitos[0])]


def test_create_user_not_found():
    repo = PrinterRepositoryNeo(FakeConnection())
    with pytest.raises(UserNotFoundError):
        repo.create_printer(make_printer())


def test_get_returns_entity():
    printer = make_printer(status=StatusPrinter.EM_USO)
    repo = PrinterRepositoryNeo(FakeConnection(rows=[row(printer)]))
    assert repo.get_printer(printer.id) == printer


def test_get_not_found():
    repo = PrinterRepositoryNeo(FakeConnection())
    with pytest.raises(PrinterNotFoundError):
        repo.get_printer(uuid7())


def test_get_all_filters_by_user():
    printer = make_printer()
    conn = FakeConnection(rows=[row(printer)])
    result = PrinterRepositoryNeo(conn).get_all_printers(printer.usuario_id)
    assert result == [printer]
    assert conn.tx.calls[0][1]["user_id"] == str(printer.usuario_id)


def test_get_all_without_user_sends_none():
    conn = FakeConnection()
    assert PrinterRepositoryNeo(conn).get_all_printers() == []
    assert conn.tx.calls[0][1]["user_id"] is None


def test_update_returns_updated_and_never_writes_relations_as_properties():
    printer = make_printer()
    conn = FakeConnection(rows=[row(printer)])
    assert PrinterRepositoryNeo(conn).update_printer(printer.id, printer) == printer
    params = conn.tx.calls[0][1]
    assert "usuario_id" not in params["printer"]
    assert "filamentos_aceitos" not in params["printer"]
    assert params["printer"]["id"] == str(printer.id)
    assert params["filament_ids"] == [str(printer.filamentos_aceitos[0])]


def test_update_not_found():
    repo = PrinterRepositoryNeo(FakeConnection())
    with pytest.raises(PrinterNotFoundError):
        repo.update_printer(uuid7(), make_printer())


def test_delete_ok_and_not_found():
    printer = make_printer()
    PrinterRepositoryNeo(FakeConnection(rows=[row(printer)])).delete_printer(printer.id)
    with pytest.raises(PrinterNotFoundError):
        PrinterRepositoryNeo(FakeConnection()).delete_printer(uuid7())


@pytest.mark.parametrize("method,args", [
    ("create_printer", lambda: (make_printer(),)),
    ("get_printer", lambda: (uuid7(),)),
    ("get_all_printers", lambda: ()),
    ("update_printer", lambda: (uuid7(), make_printer())),
    ("delete_printer", lambda: (uuid7(),)),
])
def test_driver_error_becomes_database_error(method, args):
    repo = PrinterRepositoryNeo(FakeConnection(error=RuntimeError("boom")))
    with pytest.raises(DatabaseError):
        getattr(repo, method)(*args())