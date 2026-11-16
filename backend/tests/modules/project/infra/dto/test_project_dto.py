from datetime import datetime, date, UTC
from uuid import uuid7
from pytest import fixture

from src.modules.project.domain.entities.project import Project
from src.modules.project.domain.entities.project_file import ProjectFile
from src.modules.project.domain.enums.order_status_enum import OrderStatus
from src.modules.project.infra.dto.project_dto import ProjectDTO


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
                file_url="https://example.com/a.stl"
            ),
            ProjectFile(
                title="Referência",
                file_url="https://example.com/b.pdf"
            )
        ],
        order_status={
            OrderStatus.WAITING_FOR_PARTNER: datetime(
                2026, 11, 15, tzinfo=UTC
            ),
            OrderStatus.RECEIVED: datetime(
                2026, 11, 16, tzinfo=UTC
            )
        }
    )


def test_serializes_project_properties(project):
    project_data, _, _ = ProjectDTO.entity_to_dict(project)

    assert project_data["id"] == str(project.id)
    assert project_data["date_end"] == "2026-12-15"
    assert project_data["category"] == "prosthesis"
    assert "files" not in project_data
    assert "order_status" not in project_data

def test_serializes_files_in_order(project):
    _, files_data, _ = ProjectDTO.entity_to_dict(project)

    assert len(files_data) == 2
    assert files_data[0]["title"] == "Modelo 3D"
    assert files_data[0]["position"] == 0
    assert files_data[1]["position"] == 1

def test_serializes_order_status_in_order(project):
    _, _, statuses_data = ProjectDTO.entity_to_dict(project)

    assert len(statuses_data) == 2
    assert statuses_data[0]["status"] == "waiting_for_partner"
    assert statuses_data[0]["position"] == 0
    assert statuses_data[1]["status"] == "received"
    assert statuses_data[1]["position"] == 1
    assert statuses_data[1]["timestamp"] == "2026-11-16T00:00:00+00:00"