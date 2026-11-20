from uuid import uuid7

import pytest

from src.modules.printers.domain.entities.printer import Printer
from src.modules.printers.domain.entities.status_printer import StatusPrinter
from src.modules.printers.domain.errors.printer_errors import PrinterNotFoundError
from src.modules.printers.infra.repositories.printer_repository_neo import (
    PrinterRepositoryNeo,
)
from src.shared.environments.neo4j_connection_factory import Neo4JConnectionFactory


def get_connection():
    return Neo4JConnectionFactory()


@pytest.fixture
def printer():
    return Printer(
        apelido='Ender',
        modelo='Ender 3',
        tecnologia_impressao='FDM',
        usuario_id=uuid7(),
        filamentos_aceitos=[uuid7()],
    )


class Test_PrinterRepositoryNeo:
    @pytest.mark.skip('Needs Neo4J')
    def test_create_and_get_printer(self, printer):
        repo = PrinterRepositoryNeo(connection=get_connection())
        repo.create_printer(printer)

        stored = repo.get_printer(printer.id)

        assert stored == printer
        repo.delete_printer(printer.id)

    @pytest.mark.skip('Needs Neo4J')
    def test_get_printer_not_found(self):
        repo = PrinterRepositoryNeo(connection=get_connection())
        with pytest.raises(PrinterNotFoundError):
            repo.get_printer(uuid7())

    @pytest.mark.skip('Needs Neo4J')
    def test_get_all_printers_by_user(self, printer):
        repo = PrinterRepositoryNeo(connection=get_connection())
        repo.create_printer(printer)

        result = repo.get_all_printers(printer.usuario_id)

        assert [p.id for p in result] == [printer.id]
        repo.delete_printer(printer.id)

    @pytest.mark.skip('Needs Neo4J')
    def test_update_printer(self, printer):
        repo = PrinterRepositoryNeo(connection=get_connection())
        repo.create_printer(printer)

        printer.alterar_status(StatusPrinter.EM_USO)
        updated = repo.update_printer(printer.id, printer)

        assert updated.status == StatusPrinter.EM_USO
        assert repo.get_printer(printer.id).status == StatusPrinter.EM_USO
        repo.delete_printer(printer.id)

    @pytest.mark.skip('Needs Neo4J')
    def test_update_printer_not_found(self, printer):
        repo = PrinterRepositoryNeo(connection=get_connection())
        with pytest.raises(PrinterNotFoundError):
            repo.update_printer(uuid7(), printer)

    @pytest.mark.skip('Needs Neo4J')
    def test_delete_printer(self, printer):
        repo = PrinterRepositoryNeo(connection=get_connection())
        repo.create_printer(printer)

        repo.delete_printer(printer.id)

        with pytest.raises(PrinterNotFoundError):
            repo.get_printer(printer.id)

    @pytest.mark.skip('Needs Neo4J')
    def test_delete_printer_not_found(self):
        repo = PrinterRepositoryNeo(connection=get_connection())
        with pytest.raises(PrinterNotFoundError):
            repo.delete_printer(uuid7())