from datetime import date
from unittest.mock import Mock
from uuid import uuid7

from pytest import fixture, raises

from src.modules.project.domain.entities.project import Project
from src.modules.project.domain.entities.project_file import ProjectFile
from src.modules.project.domain.repositories.project_repository_interface import IProjectRepository
from src.modules.project.infra.repositories.project_repository_neo import ProjectRepositoryNeo
from src.shared.errors.database_error import DatabaseError


@fixture
def project():
    return Project(
        id=uuid7(),
        title="Prótese de mão",
        date_end=date(2026, 12, 15),
        pieces_quantity=2,
        category="prosthesis",
        description="Projeto para reabilitação",
        urgency="high",
        filament_id=uuid7(),
        files=[
            ProjectFile(
                title="Modelo 3D",
                file_url="https://example.com/model.stl"
            )
        ]
    )


@fixture
def transaction():
    tx = Mock()
    tx.run.return_value.single.return_value = {"project": {}}
    return tx


@fixture
def connection_factory(transaction):
    conn = Mock()
    conn.execute_write.side_effect = lambda callback: callback(transaction)
    return conn


@fixture
def repo(connection_factory):
    return ProjectRepositoryNeo(connection_factory)


def test_implements_repository_interface(repo):
    assert isinstance(repo, IProjectRepository)

def test_create_project(repo, project, connection_factory):
    result = repo.create_project(project)

    assert result == project
    assert result.id.version == 7

    connection_factory.execute_write.assert_called_once()

def test_create_project_sends_correct_data(repo, project, transaction):
    repo.create_project(project)

    args, kwargs = transaction.run.call_args
    query = args[0]

    assert "CREATE (p:Project)" in query
    assert "HAS_FILE" in query
    assert "HAS_STATUS" in query

    assert kwargs["project"]["id"] == str(project.id)
    assert kwargs["files"][0]["title"] == "Modelo 3D"
    assert kwargs["statuses"][0]["status"] == "waiting_for_partner"

def test_create_project_without_result(repo, project, transaction):
    transaction.run.return_value.single.return_value = None

    with raises(DatabaseError):
        repo.create_project(project)

def test_create_project_database_error(repo, project, connection_factory):
    connection_factory.execute_write.side_effect = RuntimeError("Database connection error")

    with raises(DatabaseError):
        repo.create_project(project)