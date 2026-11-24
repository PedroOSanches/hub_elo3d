from uuid import UUID

from src.modules.filaments.domain.entities.filament import Filament
from src.modules.filaments.domain.errors.filament_errors import FilamentNotFoundError
from src.modules.filaments.domain.repositories.i_filament_repository import (
    IFilamentRepository,
)
from src.modules.filaments.infra.dto import FilamentDTO
from src.shared.environments.neo4j_connection_factory import Neo4JConnectionFactory
from src.shared.errors.database_error import DatabaseError


class FilamentRepositoryNeo(IFilamentRepository):

    def __init__(self, connection: Neo4JConnectionFactory) -> None:
        self.connection = connection

    def get_filament(self, filament_id: UUID) -> Filament:
        query = """
        MATCH (f:Filament {filament_id: $filament_id})
        RETURN properties(f) AS filament
        """

        try:
            result = self.connection.execute_read(
                lambda tx: tx.run(
                    query,
                    filament_id=str(filament_id)
                ).single()
            )
        except Exception as err:
            raise DatabaseError() from err

        if result is None:
            raise FilamentNotFoundError(filament_id=filament_id)

        return FilamentDTO().from_dict_to_entitie(result["filament"])

    def get_all_filaments(self) -> list[Filament]:
        query = """
        MATCH (f:Filament)
        RETURN properties(f) AS filament
        ORDER BY filament.tipo
        """

        try:
            result = self.connection.execute_read(
                lambda tx: tx.run(
                    query
                ).data()
            )
        except Exception as err:
            raise DatabaseError() from err

        return [
            FilamentDTO().from_dict_to_entitie(record["filament"])
            for record in result
        ]