from uuid import UUID

from src.modules.printers.domain.entities.printer import Printer
from src.modules.printers.domain.errors.printer_errors import (
    PrinterNotFoundError,
    UserNotFoundError,
)
from src.modules.printers.domain.repositories.i_printer_repository import (
    IPrinterRepository,
)
from src.modules.printers.infra.dto.printer_model import PrinterModel
from src.shared.environments.neo4j_connection_factory import Neo4JConnectionFactory
from src.shared.errors.database_error import DatabaseError

# usuário e filamentos são relacionamentos no grafo, não propriedades do nó
RELATION_FIELDS = {"usuario_id", "filamentos_aceitos"}


def _to_props(printer: Printer) -> dict:
    return PrinterModel.from_entity(printer).model_dump(
        mode="json", exclude=RELATION_FIELDS
    )


def _to_entity(record) -> Printer:
    return PrinterModel(
        **record["printer"],
        usuario_id=record["user_id"],
        filamentos_aceitos=record["filament_ids"],
    ).to_entity()


class PrinterRepositoryNeo(IPrinterRepository):
    def __init__(self, connection: Neo4JConnectionFactory) -> None:
        self.connection = connection

    def create_printer(self, printer: Printer) -> Printer:
        query = """
            MATCH (u:User {user_id: $user_id})
            CREATE (p:Printer)
            SET p = $printer
            CREATE (p)-[:HAS_PRINTER]->(u)

            WITH p
            OPTIONAL MATCH (f:Filament)
            WHERE f.filament_id IN $filament_ids
            WITH p, collect(f) AS filaments
            FOREACH (f IN filaments | CREATE (p)-[:HAS_FILAMENT]->(f))

            RETURN properties(p) AS printer
        """
        try:
            result = self.connection.execute_write(
                lambda tx: tx.run(
                    query,
                    user_id=str(printer.usuario_id),
                    filament_ids=[str(f) for f in printer.filamentos_aceitos],
                    printer=_to_props(printer),
                ).single()
            )
        except Exception as err:
            raise DatabaseError() from err

        if result is None:
            raise UserNotFoundError(printer.usuario_id)
        return printer

    def get_printer(self, printer_id: UUID) -> Printer:
        query = """
            MATCH (p:Printer {id: $printer_id})-[:HAS_PRINTER]->(u:User)
            OPTIONAL MATCH (p)-[:HAS_FILAMENT]->(f:Filament)
            RETURN
                properties(p) AS printer,
                u.user_id AS user_id,
                collect(f.filament_id) AS filament_ids
        """
        try:
            result = self.connection.execute_read(
                lambda tx: tx.run(query, printer_id=str(printer_id)).single()
            )
        except Exception as err:
            raise DatabaseError() from err

        if result is None:
            raise PrinterNotFoundError(printer_id)
        return _to_entity(result)

    def get_all_printers(self, user_id: UUID | None = None) -> list[Printer]:
        query = """
            MATCH (p:Printer)-[:HAS_PRINTER]->(u:User)
            WHERE $user_id IS NULL OR u.user_id = $user_id
            OPTIONAL MATCH (p)-[:HAS_FILAMENT]->(f:Filament)
            RETURN
                properties(p) AS printer,
                u.user_id AS user_id,
                collect(f.filament_id) AS filament_ids
            ORDER BY printer.id
        """
        uid = str(user_id) if user_id is not None else None
        try:
            records = self.connection.execute_read(
                lambda tx: list(tx.run(query, user_id=uid))
            )
        except Exception as err:
            raise DatabaseError() from err

        return [_to_entity(r) for r in records]

    def update_printer(self, printer_id: UUID, updated_printer: Printer) -> Printer:
        query = """
            MATCH (p:Printer {id: $printer_id})-[:HAS_PRINTER]->(u:User)
            SET p += $printer

            WITH p, u
            OPTIONAL MATCH (p)-[old:HAS_FILAMENT]->(:Filament)
            WITH p, u, collect(old) AS olds
            FOREACH (r IN olds | DELETE r)

            WITH p, u
            OPTIONAL MATCH (f:Filament)
            WHERE f.filament_id IN $filament_ids
            WITH p, u, collect(f) AS filaments
            FOREACH (f IN filaments | CREATE (p)-[:HAS_FILAMENT]->(f))

            RETURN
                properties(p) AS printer,
                u.user_id AS user_id,
                [f IN filaments | f.filament_id] AS filament_ids
        """
        props = _to_props(updated_printer)
        props["id"] = str(printer_id)  # id nunca muda
        try:
            result = self.connection.execute_write(
                lambda tx: tx.run(
                    query,
                    printer_id=str(printer_id),
                    filament_ids=[str(f) for f in updated_printer.filamentos_aceitos],
                    printer=props,
                ).single()
            )
        except Exception as err:
            raise DatabaseError() from err

        if result is None:
            raise PrinterNotFoundError(printer_id)
        return _to_entity(result)

    def delete_printer(self, printer_id: UUID) -> None:
        query = """
            MATCH (p:Printer {id: $printer_id})
            WITH p, properties(p) AS printer
            DETACH DELETE p
            RETURN printer
        """
        try:
            result = self.connection.execute_write(
                lambda tx: tx.run(query, printer_id=str(printer_id)).single()
            )
        except Exception as err:
            raise DatabaseError() from err

        if result is None:
            raise PrinterNotFoundError(printer_id)