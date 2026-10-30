import json
from datetime import date
from uuid import UUID, uuid4

from src.modules.project.application.web.schemas.create_project_schema import (CreateProjectRequestSchema, CreateProjectResponseSchema)
from src.modules.project.domain.entities.project import Project

def valid_project():
    request = CreateProjectRequestSchema(
        title="Prótese de mão",
        date_end="2026-11-15",
        pieces_quantity=1,
        category="Ortopedia",
        description="Prótese para reabilitação",
        urgency="high",
        filament_id=str(uuid4()),
        files=[
            {
                "title": "Modelo 3D",
                "file_url": "https://example.com/model.stl"
            }
        ]
    )

    return Project(**request.model_dump())

class TestCreateProjectResponseSchema:
    def test_create_response(self):
        project = valid_project()
        response = CreateProjectResponseSchema.model_validate(project)

        assert response.id == project.id
        assert response.title == "Prótese de mão"
        assert response.order_status == "waiting_for_partner"
        assert response.printer_id is None

    def test_response_json_serialization(self):
        project = valid_project()
        response = CreateProjectResponseSchema.model_validate(project)
        data = response.model_dump(mode="json")

        assert data["id"] == str(project.id)
        assert data["date_end"] == "2026-11-15"
        assert data["urgency"] == "high"
        assert data["files"][0]["title"] == "Modelo 3D"

        json.dumps(data)

    def test_response_with_printer(self):
        project = valid_project()
        printer_id = uuid4()
        project.printer_id = printer_id
        response = CreateProjectResponseSchema.model_validate(project)

        assert response.printer_id == printer_id