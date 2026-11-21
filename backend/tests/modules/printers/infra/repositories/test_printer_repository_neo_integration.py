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
from src.shared.environments.neo4j_connection_factory import Neo4JConnectionFactory


@pytest.fixture
def connection():
    return Neo4JConnectionFactory()


@pytest.fixture
def repo(connection):
    return PrinterRepositoryNeo(connection=connection)


@pytest.fixture
def printer(connection):
    # o create exige o User no banco; os Filaments são ligados se existirem
    user_id, filament_id = uuid7(), uuid7()
    connection.execute_write(lambda tx: tx.run(
        """
        CREATE (:User {user_id: $user_id})
        CREATE (:Filament {filament_id: $filament_id})
        """,
        user_id=str(user_id),
        filament_id=str(filament_id),
    ).consume())

    yield Printer(
        apelido='Ender',
        modelo='Ender 3',
        tecnologia_impressao='FDM',
        usuario_id=user_id,
        filamentos_aceitos=[filament_id],
    )

    # remove impressora, usuário e filamento de teste
    connection.execute_write(lambda tx: tx.run(
        """
        OPTIONAL MATCH (p:Printer)-[:HAS_PRINTER]->(u:User {user_id: $user_id})
        OPTIONAL MATCH (f:Filament {filament_id: $filament_id})
        DETACH DELETE p, u, f
        """,
        user_id=str(user_id),
        filament_id=str(filament_id),
    ).consume())


class Test_PrinterRepositoryNeo:
    @pytest.mark.skip('Needs Neo4J')
    def test_create_and_get_printer(self, repo, printer):
        repo.create_printer(printer)

        stored = repo.get_printer(printer.id)

        assert stored == printer
        assert stored.usuario_id == printer.usuario_id
        assert stored.filamentos_aceitos == printer.filamentos_aceitos

    @pytest.mark.skip('Needs Neo4J')
    def test_create_printer_user_not_found(self, repo, printer):
        printer.usuario_id = uuid7()

        with pytest.raises(UserNotFoundError):
            repo.create_printer(printer)

    @pytest.mark.skip('Needs Neo4J')
    def test_get_printer_not_found(self, repo):
        with pytest.raises(PrinterNotFoundError):
            repo.get_printer(uuid7())

    @pytest.mark.skip('Needs Neo4J')
    def test_get_all_printers_by_user(self, repo, printer):
        repo.create_printer(printer)

        result = repo.get_all_printers(printer.usuario_id)

        assert [p.id for p in result] == [printer.id]

    @pytest.mark.skip('Needs Neo4J')
    def test_get_all_printers_other_user_sees_nothing(self, repo, printer):
        repo.create_printer(printer)

        assert repo.get_all_printers(uuid7()) == []

    @pytest.mark.skip('Needs Neo4J')
    def test_update_printer(self, repo, printer):
        repo.create_printer(printer)

        printer.alterar_status(StatusPrinter.EM_USO)
        updated = repo.update_printer(printer.id, printer)

        assert updated.status == StatusPrinter.EM_USO
        assert repo.get_printer(printer.id).status == StatusPrinter.EM_USO

    @pytest.mark.skip('Needs Neo4J')
    def test_update_printer_removes_filaments(self, repo, printer):
        repo.create_printer(printer)

        printer.filamentos_aceitos = []
        repo.update_printer(printer.id, printer)

        assert repo.get_printer(printer.id).filamentos_aceitos == []

    @pytest.mark.skip('Needs Neo4J')
    def test_update_printer_not_found(self, repo, printer):
        with pytest.raises(PrinterNotFoundError):
            repo.update_printer(uuid7(), printer)

    @pytest.mark.skip('Needs Neo4J')
    def test_delete_printer(self, repo, printer):
        repo.create_printer(printer)

        repo.delete_printer(printer.id)

        with pytest.raises(PrinterNotFoundError):
            repo.get_printer(printer.id)

    @pytest.mark.skip('Needs Neo4J')
    def test_delete_printer_not_found(self, repo):
        with pytest.raises(PrinterNotFoundError):
            repo.delete_printer(uuid7())