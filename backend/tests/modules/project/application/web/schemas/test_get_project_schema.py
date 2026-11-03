from datetime import date
from uuid import uuid4
from pytest import fixture, raises
from pydantic import ValidationError

from src.modules.project.domain.entities.project import Project
from src.modules.project.domain.entities.project_file import ProjectFile
from src.modules.project.application.web.schemas.get_project_schema import GetProjectResponseSchema

@fixture
def valid_project():
    return Project(
        id=uuid4(),
        title="Prótese de mão",
        date_end=date(2026, 11, 15),
        pieces_quantity=1,
        category="Ortopedia",
        description="Projeto para reabilitação",
        technical_info=None,
        urgency="high",
        filament_id=uuid4(),
        files=[
            ProjectFile(
                title="Modelo 3D",
                file_url="https://example.com/model.stl"
            )
        ]
    )

class TestGetProjectResponseSchema:
    def test_create_response_from_valid_project(self, valid_project):
        response = GetProjectResponseSchema.model_validate(valid_project)
        
        assert response.id == valid_project.id
        assert response.title == valid_project.title
        assert response.pieces_quantity == 1
        assert len(response.files) == 1

    def test_serialize_response_to_json(self, valid_project):
        response = GetProjectResponseSchema.model_validate(valid_project)
        data = response.model_dump(mode="json")

        assert data["id"] == str(valid_project.id)
        assert data["date_end"] == "2026-11-15"
        assert data["order_status"] == "waiting_for_partner"
        assert data["urgency"] == "high"
        assert data["files"][0]["title"] == "Modelo 3D"

    def test_response_requires_title(self, valid_project):
        valid_project.title = None

        with raises(ValidationError):
            GetProjectResponseSchema.model_validate(valid_project)