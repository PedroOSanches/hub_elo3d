import os
from datetime import date
from urllib.parse import urlparse
from uuid import uuid7

from pytest import fixture, skip, fail, raises

from src.modules.project.domain.entities.project import Project
from src.modules.project.domain.entities.project_file import ProjectFile
from src.modules.project.infra.repositories.project_repository_neo import ProjectRepositoryNeo
from src.shared.environments.environments import env
from src.shared.environments.neo4j_connection_factory import Neo4JConnectionFactory
from src.modules.project.domain.enums.order_status_enum import OrderStatus
from src.modules.project.domain.errors.project_errors import (
    NoProjectsAvailable,
    ProjectNotFoundError,
)


@fixture
def repo(monkeypatch):
    uri = os.getenv("NEO4J_TEST_URI")
    user = os.getenv("NEO4J_TEST_USER")
    password = os.getenv("NEO4J_TEST_PASSWORD")
    database = os.getenv("NEO4J_TEST_DATABASE", "neo4j")

    if not all([uri, user, password]):
        skip("Neo4j de testes não configurado")

    if urlparse(uri).hostname not in ("localhost", "127.0.0.1"):
        fail("Os testes devem usar um Neo4j local")

    monkeypatch.setattr(env, "neo_uri", uri)
    monkeypatch.setattr(env, "neo_user", user)
    monkeypatch.setattr(env, "neo_pass", password)
    monkeypatch.setattr(env, "neo_database", database)

    conn = Neo4JConnectionFactory()

    try:
        conn.driver.verify_connectivity()
        yield ProjectRepositoryNeo(conn)
    finally:
        conn.close()


@fixture
def project():
    return Project(
        id=uuid7(),
        title="Projeto de integração",
        date_end=date(2026, 12, 31),
        pieces_quantity=1,
        category="prosthesis",
        description="Teste de persistência no Neo4j",
        urgency="high",
        filament_id=uuid7(),
        files=[
            ProjectFile(
                title="Modelo 3D",
                object_key=uuid7(),
                size=2048,
                content_type="model/stl"
            )
        ]
    )


def test_create_and_get_project_real_db(repo, project):
    try:
        created = repo.create_project(project)
        retrieved = repo.get_project(project.id)

        assert created == project
        assert retrieved == project
        assert retrieved.files == project.files
        assert retrieved.order_status == project.order_status

    finally:
        repo.connection_factory.execute_write(
            lambda tx: tx.run(
                """
                MATCH (p:Project {id: $project_id})

                OPTIONAL MATCH (p)-[:HAS_FILE|HAS_STATUS]->(child)

                WITH p, collect(DISTINCT child) AS children

                FOREACH (child IN children |
                    DETACH DELETE child
                )

                DETACH DELETE p
                """,
                project_id=str(project.id)
            ).consume()
        )

def test_get_all_projects_real_db(repo, project):
    second_project = project.model_copy(
        update={
            "id": uuid7(),
            "title": "Segundo projeto de integração",
            "files": [
                ProjectFile(
                    title="Segundo modelo",
                    object_key='project/project_name/uuid.stl',
                    size=1024,
                    content_type="model/stl"
                )
            ],
        },
        deep=True
    )

    projects_ids = [str(project.id), str(second_project.id)]

    try:
        repo.create_project(project)
        repo.create_project(second_project)

        results = repo.get_all_projects()

        projects_by_id = {
            item.id: item
            for item in results
        }

        assert projects_by_id[project.id] == project
        assert projects_by_id[second_project.id] == second_project

    finally:
        repo.connection_factory.execute_write(
            lambda tx: tx.run(
                """
                MATCH (p:Project)
                WHERE p.id IN $projects_ids

                OPTIONAL MATCH
                    (p)-[:HAS_FILE|HAS_STATUS]->(child)

                WITH
                    collect(DISTINCT p) AS projects,
                    collect(DISTINCT child) AS children

                FOREACH (child IN children |
                    DETACH DELETE child
                )

                FOREACH (p IN projects |
                    DETACH DELETE p
                )
                """,
                projects_ids=projects_ids
            ).consume()
        )

def test_available_projects_real_db(repo, project):
    user_id = uuid7()
    printer_id = uuid7()

    try:
        repo.create_project(project)

        repo.connection_factory.execute_write(
            lambda tx: tx.run(
                """
                MATCH (f:Filament {filament_id: $filament_id})
                MERGE (u:User {user_id: $user_id})
                CREATE (u)-[:HAS_PRINTER]->(
                    printer:Printer {
                        id: $printer_id,
                        status: 'disponivel'
                    }
                )
                CREATE (printer)-[:HAS_FILAMENT]->(f)
                """,
                filament_id=str(project.filament_id),
                user_id=str(user_id),
                printer_id=str(printer_id)
            ).consume()
        )

        result = repo.available_projects(user_id)

        assert len(result) == 1
        assert result[0] == project

    finally:
        repo.connection_factory.execute_write(
            lambda tx: tx.run(
                """
                MATCH (p:Project {id: $project_id})
                OPTIONAL MATCH
                    (p)-[:HAS_FILE|HAS_STATUS|USES_FILAMENT]->(child)

                WITH p, collect(DISTINCT child) AS children

                FOREACH (child IN children |
                    DETACH DELETE child
                )

                DETACH DELETE p
                """,
                project_id=str(project.id)
            ).consume()
        )

        repo.connection_factory.execute_write(
            lambda tx: tx.run(
                """
                MATCH (u:User {user_id: $user_id})
                OPTIONAL MATCH (u)-[:HAS_PRINTER]->(printer:Printer)
                WHERE printer.id = $printer_id

                OPTIONAL MATCH (printer)-[:HAS_FILAMENT]->(filament:Filament)

                DETACH DELETE u, printer, filament
                """,
                user_id=str(user_id),
                printer_id=str(printer_id)
            ).consume()
        )

def test_available_projects_empty_real_db(repo):
    with raises(NoProjectsAvailable):
        repo.available_projects(uuid7())

def test_update_project_real_db(repo, project):
    original_file_key = str(project.files[0].object_key)

    updated = project.model_copy(
        update={
            "title": "Projeto atualizado",
            "pieces_quantity": 3,
            "files": [
                ProjectFile(
                    title="Modelo atualizado",
                    object_key='project/project_name/uuid.stl',
                    size=4096,
                    content_type="model/stl"
                )
            ],
        },
        deep=True
    )

    updated.register_order_status(OrderStatus.RECEIVED)

    try:
        repo.create_project(project)

        result = repo.update_project(project.id, updated)
        retrieved = repo.get_project(project.id)

        assert result == updated
        assert retrieved == updated
        assert retrieved.title == "Projeto atualizado"
        assert retrieved.pieces_quantity == 3
        assert retrieved.files == updated.files
        assert retrieved.order_status == updated.order_status
        assert len(retrieved.order_status) == 2

        old_files_count = repo.connection_factory.execute_read(
            lambda tx: tx.run(
                """
                MATCH (f:ProjectFile {object_key: $object_key})
                RETURN count(f) AS total
                """,
                object_key=original_file_key
            ).single()["total"]
        )

        assert old_files_count == 0

    finally:
        repo.connection_factory.execute_write(
            lambda tx: tx.run(
                """
                MATCH (p:Project {id: $project_id})
                OPTIONAL MATCH
                    (p)-[:HAS_FILE|HAS_STATUS]->(child)

                WITH p, collect(DISTINCT child) AS children

                FOREACH (child IN children |
                    DETACH DELETE child
                )

                DETACH DELETE p
                """,
                project_id=str(project.id)
            ).consume()
        )

def test_delete_project_real_db(repo, project):
    project_id = str(project.id)

    try:
        repo.create_project(project)

        related_ids = repo.connection_factory.execute_read(
            lambda tx: [
                record["node_id"]
                for record in tx.run(
                    """
                    MATCH (p:Project {id: $project_id})
                          -[:HAS_FILE|HAS_STATUS]->(child)

                    RETURN elementId(child) AS node_id
                    """,
                    project_id=project_id
                )
            ]
        )

        assert len(related_ids) == (
            len(project.files) + len(project.order_status)
        )

        deleted = repo.delete_project(project.id)

        assert deleted == project

        with raises(ProjectNotFoundError):
            repo.get_project(project.id)

        remaining = repo.connection_factory.execute_read(
            lambda tx: tx.run(
                """
                MATCH (n)
                WHERE elementId(n) IN $node_ids

                RETURN count(n) AS total
                """,
                node_ids=related_ids
            ).single()["total"]
        )

        assert remaining == 0

    finally:
        repo.connection_factory.execute_write(
            lambda tx: tx.run(
                """
                MATCH (p:Project {id: $project_id})
                OPTIONAL MATCH
                    (p)-[:HAS_FILE|HAS_STATUS]->(child)

                WITH p, collect(DISTINCT child) AS children

                FOREACH (child IN children |
                    DETACH DELETE child
                )

                DETACH DELETE p
                """,
                project_id=project.id
            ).consume()
        )

def test_delete_project_not_found_real_db(repo, project):
    with raises(ProjectNotFoundError):
        repo.delete_project(project.id)