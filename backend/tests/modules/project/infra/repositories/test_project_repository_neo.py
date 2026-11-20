from datetime import date
from unittest.mock import Mock
from uuid import uuid7

from pytest import fixture, raises

from src.modules.project.domain.entities.project import Project
from src.modules.project.domain.entities.project_file import ProjectFile
from src.modules.project.domain.repositories.project_repository_interface import IProjectRepository
from src.modules.project.infra.repositories.project_repository_neo import ProjectRepositoryNeo
from src.shared.errors.database_error import DatabaseError
from src.modules.project.domain.errors.project_errors import ProjectNotFoundError
from src.modules.project.infra.dto.project_dto import ProjectDTO
from src.modules.project.domain.enums.order_status_enum import OrderStatus


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
                object_key=uuid7(),
                size=2048,
                content_type="model/stl"
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
    conn.execute_read.side_effect = lambda callback: callback(transaction)
    return conn


@fixture
def repo(connection_factory):
    return ProjectRepositoryNeo(connection_factory)


def test_implements_repository_interface(repo):
    assert isinstance(repo, IProjectRepository)

def test_create_project(
    repo, project, connection_factory
):
    result = repo.create_project(project)

    assert result == project
    assert result.id.version == 7

    connection_factory.execute_write.assert_called_once()

def test_create_project_sends_correct_data(
    repo, project, transaction
):
    repo.create_project(project)

    args, kwargs = transaction.run.call_args
    query = args[0]

    assert "CREATE (p:Project)" in query
    assert "HAS_FILE" in query
    assert "HAS_STATUS" in query

    assert kwargs["project"]["id"] == str(project.id)
    assert kwargs["files"][0]["title"] == "Modelo 3D"
    assert kwargs["statuses"][0]["status"] == "waiting_for_partner"

def test_create_project_without_result(
    repo, project, transaction
):
    transaction.run.return_value.single.return_value = None

    with raises(DatabaseError):
        repo.create_project(project)

def test_create_project_database_error(
    repo, project, connection_factory
):
    connection_factory.execute_write.side_effect = RuntimeError("Database connection error")

    with raises(DatabaseError):
        repo.create_project(project)

def test_get_project(
    repo, project, transaction, connection_factory
):
    project_data, files_data, statuses_data = (
        ProjectDTO.entity_to_dict(project)
    )

    record = Mock()
    record.data.return_value = {
        "project": project_data,
        "files": files_data,
        "statuses": statuses_data
    }

    transaction.run.return_value.single.return_value = record

    result = repo.get_project(project.id)

    assert result == project
    assert result.id.version == 7

    connection_factory.execute_read.assert_called_once()

    args, kwargs = transaction.run.call_args

    assert "MATCH (p:Project" in args[0]
    assert kwargs["project_id"] == str(project.id)

def test_get_project_not_found(
    repo, project, transaction
):
    transaction.run.return_value.single.return_value = None

    with raises(ProjectNotFoundError):
        repo.get_project(project.id)

def test_get_project_database_error(
    repo, project, connection_factory
):
    connection_factory.execute_read.side_effect = RuntimeError(
        "Database connection error"
    )

    with raises(DatabaseError):
        repo.get_project(project.id)

def test_get_all_projects(
    repo, project, transaction, connection_factory
):
    second_project = project.model_copy(
        update={
            "id": uuid7(),
            "title": "Prótese de perna"
        },
        deep=True
    )

    results = []

    for item in [project, second_project]:
        project_data, files_data, statuses_data = (
            ProjectDTO.entity_to_dict(item)
        )

        result = Mock()
        result.data.return_value = {
            "project": project_data,
            "files": files_data,
            "statuses": statuses_data
        }
        results.append(result)

    transaction.run.return_value = results

    result = repo.get_all_projects()

    assert result == [project, second_project]
    assert len(result) == 2

    connection_factory.execute_read.assert_called_once()

    args, kwargs = transaction.run.call_args

    assert "ORDER BY project.id" in args[0]

def test_get_all_projects_empty(
    repo, transaction
):
    transaction.run.return_value = []

    result = repo.get_all_projects()

    assert result == []

def test_get_all_projects_database_error(
    repo, connection_factory
):
    connection_factory.execute_read.side_effect = RuntimeError(
        "Database connection error"
    )

    with raises(DatabaseError):
        repo.get_all_projects()

def test_update_project(
    repo, project, connection_factory
):
    updated = project.model_copy(
        update={"title": "Prótese de mão atualizada"},
        deep=True
    )

    result = repo.update_project(project.id, updated)

    assert result == updated
    assert result.id == project.id

    connection_factory.execute_write.assert_called_once()

def test_update_project_sends_correct_data(
    repo, project, transaction
):
    updated = project.model_copy(deep=True)
    updated.register_order_status(OrderStatus.RECEIVED)

    repo.update_project(project.id, updated)

    args, kwargs = transaction.run.call_args
    query = args[0]

    assert "MATCH (p:Project" in query
    assert "DETACH DELETE old" in query
    assert "HAS_FILE" in query
    assert "HAS_STATUS" in query

    assert kwargs["project_id"] == str(project.id)
    assert kwargs["project"]["id"] == str(project.id)
    assert kwargs["files"][0]["object_key"] == str(
        project.files[0].object_key
    )

    assert len(kwargs["statuses"]) == 2
    assert kwargs["statuses"][1]["status"] == "received"

def test_update_project_not_found(
    repo, project, transaction
):
    transaction.run.return_value.single.return_value = None

    with raises(ProjectNotFoundError):
        repo.update_project(project.id, project)

def test_update_project_different_id(
    repo, project, connection_factory
):
    updated = project.model_copy(
        update={"id": uuid7()},
        deep=True
    )

    with raises(ValueError, match="Project ID mismatch"):
        repo.update_project(project.id, updated)

    connection_factory.execute_write.assert_not_called()

def test_update_project_database_error(
    repo, project, connection_factory
):
    connection_factory.execute_write.side_effect = RuntimeError(
        "Database connection error"
    )

    with raises(DatabaseError):
        repo.update_project(project.id, project)

def test_delete_project(
    repo, project, transaction, connection_factory
):
    project_data, files_data, statuses_data = (
        ProjectDTO.entity_to_dict(project)
    )

    record = Mock()
    record.data.return_value = {
        "project": project_data,
        "files": files_data,
        "statuses": statuses_data
    }

    transaction.run.return_value.single.return_value = record

    result = repo.delete_project(project.id)

    assert result == project

    connection_factory.execute_write.assert_called_once()

def test_delete_project_not_found(
    repo, project, transaction
):
    transaction.run.return_value.single.return_value = None

    with raises(ProjectNotFoundError):
        repo.delete_project(project.id)

def test_delete_project_database_error(
    repo, project, connection_factory
):
    connection_factory.execute_write.side_effect = RuntimeError(
        "Database connection error"
    )

    with raises(DatabaseError):
        repo.delete_project(project.id)