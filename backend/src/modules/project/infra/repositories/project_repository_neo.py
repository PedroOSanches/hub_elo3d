from uuid import UUID

from src.modules.project.domain.entities.project import Project
from src.modules.project.domain.repositories.project_repository_interface import (
    IProjectRepository,
)
from src.modules.project.infra.dto.project_dto import ProjectDTO
from src.shared.environments.neo4j_connection_factory import Neo4JConnectionFactory
from src.shared.errors.database_error import DatabaseError


class ProjectRepositoryNeo(IProjectRepository):

    def __init__(self, connection_factory: Neo4JConnectionFactory):
        self.connection_factory = connection_factory

    def create_project(self, project: Project) -> Project:
        query = """
            CREATE (p:Project)
            SET p = $project

            FOREACH (file IN $files |
                CREATE (f:ProjectFile)
                SET f = file
                CREATE (p)-[:HAS_FILE]->(f)
            )

            FOREACH (status IN $statuses |
                CREATE (s:ProjectStatus)
                SET s = status
                CREATE (p)-[:HAS_STATUS]->(s)
            )

            RETURN p
        """

        project_data, files_data, statuses_data = (
            ProjectDTO.entity_to_dict(project)
        )

        try:
            result = self.connection_factory.execute_write(
                lambda tx: tx.run(
                    query,
                    project=project_data,
                    files=files_data,
                    statuses=statuses_data,
                ).single()
            )
        except Exception as e:
            raise DatabaseError() from e

        if result is None:
            raise DatabaseError()

        return project

    def get_project(
        self,
        project_id: UUID
    ) -> Project:
        raise NotImplementedError

    def get_all_projects(
        self
    ) -> list[Project]:
        raise NotImplementedError

    def update_project(
        self,
        project_id: UUID,
        updated_project: Project
    ) -> Project:
        raise NotImplementedError

    def delete_project(
        self,
        project_id: UUID
    ) -> Project:
        raise NotImplementedError