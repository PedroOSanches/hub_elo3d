import os
from datetime import date
from urllib.parse import urlparse
from uuid import uuid7

from pytest import fixture, skip, fail

from src.modules.project.domain.entities.project import Project
from src.modules.project.domain.entities.project_file import ProjectFile
from src.modules.project.infra.repositories.project_repository_neo import ProjectRepositoryNeo
from src.shared.environments.environments import env
from src.shared.environments.neo4j_connection_factory import Neo4JConnectionFactory


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
                content_type="model/stl",
            )
        ],
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
                OPTIONAL MATCH
                    (p)-[:HAS_FILE|HAS_STATUS]->(child)
                WITH p, collect(DISTINCT child) AS children

                FOREACH (child IN children |
                    DETACH DELETE child
                )

                DETACH DELETE p
                """,
                project_id=str(project.id),
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
                    object_key=uuid7(),
                    size=1024,
                    content_type="model/stl",
                )
            ],
        },
        deep=True,
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
                projects_ids=projects_ids,
            ).consume()
        )