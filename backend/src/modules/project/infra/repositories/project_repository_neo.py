from uuid import UUID

from src.modules.project.domain.entities.project import Project
from src.modules.project.domain.errors.project_errors import ProjectNotFoundError
from src.modules.project.domain.repositories.project_repository_interface import (
    IProjectRepository,
)
from src.modules.project.infra.dto.project_dto import ProjectDTO
from src.shared.environments.neo4j_connection_factory import Neo4JConnectionFactory
from src.shared.errors.database_error import DatabaseError


class ProjectRepositoryNeo(IProjectRepository):

    def __init__(self, connection_factory: Neo4JConnectionFactory):
        self.connection_factory = connection_factory

    def create_project(
            self,
            project: Project
    ) -> Project:
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
        query = """
            MATCH (p:Project {id: $project_id})

            OPTIONAL MATCH (p)-[:HAS_FILE]->(f:ProjectFile)
            WITH p, collect(properties(f)) AS files

            OPTIONAL MATCH (p)-[:HAS_STATUS]->(s:ProjectStatus)

            RETURN
                properties(p) AS project,
                files,
                collect(properties(s)) AS statuses
        """

        try:
            result = self.connection_factory.execute_read(
                lambda tx: tx.run(
                    query,
                    project_id=str(project_id)
                ).single()
            )
        except Exception as e:
            raise DatabaseError() from e

        if result is None:
            raise ProjectNotFoundError(project_id)

        data = result.data()

        return ProjectDTO.dict_to_entity(
            project_data=data["project"],
            files_data=data["files"],
            statuses_data=data["statuses"]
        )

    def get_all_projects(
        self
    ) -> list[Project]:
        query = """
            MATCH (p:Project)

            OPTIONAL MATCH (p)-[:HAS_FILE]->(f:ProjectFile)
            WITH p, collect(properties(f)) AS files

            OPTIONAL MATCH (p)-[:HAS_STATUS]->(s:ProjectStatus)

            RETURN
                properties(p) AS project,
                files,
                collect(properties(s)) AS statuses
            ORDER BY p.id
        """

        try:
            results = self.connection_factory.execute_read(
                lambda tx: [
                    result.data()
                    for result in tx.run(query)
                ]
            )
        except Exception as e:
            raise DatabaseError() from e

        return [
            ProjectDTO.dict_to_entity(
                project_data=data["project"],
                files_data=data["files"],
                statuses_data=data["statuses"]
            )
            for data in results
        ]

    def update_project(
        self,
        project_id: UUID,
        updated_project: Project
    ) -> Project:
        
        if updated_project.id != project_id:
            raise ValueError("Project ID mismatch")

        query = """
            MATCH (p:Project {id: $project_id})

            OPTIONAL MATCH (p)-[:HAS_FILE|HAS_STATUS]->(old)
            WITH p, collect(DISTINCT old) AS old_nodes

            FOREACH (old IN old_nodes |
                DETACH DELETE old
            )

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
            ProjectDTO.entity_to_dict(updated_project)
        )

        try:
            result = self.connection_factory.execute_write(
                lambda tx: tx.run(
                    query,
                    project_id=str(project_id),
                    project=project_data,
                    files=files_data,
                    statuses=statuses_data,
                ).single()
            )
        except Exception as e:
            raise DatabaseError() from e

        if result is None:
            raise ProjectNotFoundError(project_id)

        return updated_project

    def delete_project(
        self,
        project_id: UUID
    ) -> Project:
        query = """
            MATCH (p:Project {id: $project_id})

            OPTIONAL MATCH (p)-[:HAS_FILE]->(f:ProjectFile)
            WITH
                p,
                collect(f) AS file_nodes,
                collect(properties(f)) AS files

            OPTIONAL MATCH (p)-[:HAS_STATUS]->(s:ProjectStatus)
            WITH
                p,
                file_nodes,
                files,
                collect(s) AS status_nodes,
                collect(properties(s)) AS statuses

            WITH
                p,
                file_nodes + status_nodes AS nodes,
                properties(p) AS project,
                files,
                statuses

            FOREACH (node IN nodes |
                DETACH DELETE node
            )

            DETACH DELETE p

            RETURN project, files, statuses
        """

        try:
            result = self.connection_factory.execute_write(
                lambda tx: tx.run(
                    query,
                    project_id=str(project_id)
                ).single()
            )
        except Exception as e:
            raise DatabaseError() from e

        if result is None:
            raise ProjectNotFoundError(project_id)

        data = result.data()

        return ProjectDTO.dict_to_entity(
            project_data=data["project"],
            files_data=data["files"],
            statuses_data=data["statuses"]
        )