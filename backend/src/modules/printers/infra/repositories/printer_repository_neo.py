from uuid import UUID

from src.modules.printers.domain.entities.printer import Printer
from src.modules.printers.domain.errors.printer_errors import PrinterNotFoundError
from src.modules.printers.domain.repositories.i_printer_repository import (
    IPrinterRepository,
)
from src.modules.printers.infra.dto.printer_model import PrinterModel
from src.shared.environments.neo4j_connection_factory import Neo4JConnectionFactory
from src.shared.errors.database_error import DatabaseError


def _to_props(printer: Printer) -> dict:
    return PrinterModel.from_entity(printer).model_dump(mode="json")


class PrinterRepositoryNeo(IPrinterRepository):
    def __init__(self, connection: Neo4JConnectionFactory) -> None:
        self.connection = connection

    def create_printer(self, printer: Printer) -> Printer:
        query = """
            CREATE (p:Printer)
            SET p = $printer
            RETURN properties(p) AS printer
        """
        try:
            self.connection.execute_write(
                lambda tx: tx.run(query, printer=_to_props(printer)).single()
            )
            
        except Exception as err:
            raise DatabaseError() from err
        return printer

    def get_printer(self, printer_id: UUID) -> Printer:
        query = """
            MATCH (p:Printer {id: $printer_id})
            RETURN properties(p) AS printer
        """
        try:
            result = self.connection.execute_read(
                lambda tx: tx.run(query, printer_id=str(printer_id)).single()
            )
            
        except Exception as err:
            raise DatabaseError() from err

        if result is None:
            raise PrinterNotFoundError(printer_id)
        return PrinterModel(**result["printer"]).to_entity()

    def get_all_printers(self, user_id: UUID | None = None) -> list[Printer]:
        query = """
            MATCH (p:Printer)
            WHERE $user_id IS NULL OR p.usuario_id = $user_id
            RETURN properties(p) AS printer
            ORDER BY p.id
        """
        uid = str(user_id) if user_id is not None else None
        
        try:
            records = self.connection.execute_read(
                lambda tx: list(tx.run(query, user_id=uid))
            )
            
        except Exception as err:
            raise DatabaseError() from err

        return [PrinterModel(**r["printer"]).to_entity() for r in records]

    def update_printer(self, printer_id: UUID, updated_printer: Printer) -> Printer:
        query = """
            MATCH (p:Printer {id: $printer_id})
            SET p += $printer
            RETURN properties(p) AS printer
        """
        props = _to_props(updated_printer)
        props["id"] = str(printer_id)
        
        try:
            result = self.connection.execute_write(
                lambda tx: tx.run(
                    query, printer_id=str(printer_id), printer=props
                ).single()
            )
            
        except Exception as err:
            raise DatabaseError() from err

        if result is None:
            raise PrinterNotFoundError(printer_id)
        return PrinterModel(**result["printer"]).to_entity()

    def delete_printer(self, printer_id: UUID) -> None:
        query = """
            MATCH (p:Printer {id: $printer_id})
            DETACH DELETE p
            RETURN count(p) AS deleted
        """
        
        try:
            result = self.connection.execute_write(
                lambda tx: tx.run(query, printer_id=str(printer_id)).single()
            )
            
        except Exception as err:
            raise DatabaseError() from err

        if result is None or result["deleted"] == 0:
            raise PrinterNotFoundError(printer_id)