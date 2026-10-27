from datetime import date
from uuid import UUID

from pytest import raises
from pydantic import ValidationError

from src.modules.project.application.web.schemas.create_project_schema import CreateProjectRequestSchema

def valid_request_data(**overrides):
    data = {
        "title": "Prótese de mão",
        "date_end": "2026-11-15",
        "pieces_quantity": 2,
        "category": "Ortopedia",
        "description": "Modelo de prótese para reabilitação",
        "urgency": "high",
        "filament_id": "123e4567-e89b-12d3-a456-426614174000",
        "files": [
            {
                "title": "Modelo 3D",
                "file_url": "https://example.com/model.stl"
            }
        ]
    }

    data.update(overrides)
    return data

class TestCreateProjectRequestSchema:
    def test_valid_request(self):
        request = CreateProjectRequestSchema(**valid_request_data())

        assert request.title == "Prótese de mão"
        assert request.date_end == date(2026, 11, 15)
        assert request.pieces_quantity == 2
        assert request.urgency.value == "high"
        assert request.filament_id == UUID("123e4567-e89b-12d3-a456-426614174000")
        assert request.files[0].title == "Modelo 3D"

    def test_required_files(self):
        with raises(ValidationError):
            CreateProjectRequestSchema(**valid_request_data(files=[]))

    def test_invalid_quantity(self):
        with raises(ValidationError):
            CreateProjectRequestSchema(**valid_request_data(pieces_quantity=0))

    def test_description_only_spaces(self):
        with raises(ValidationError):
            CreateProjectRequestSchema(**valid_request_data(description="     "))

    def test_description_is_normalized(self):
        request = CreateProjectRequestSchema(
            **valid_request_data(description="  Prótese de mão  "))

        assert request.description == "Prótese de mão"

    def test_invalid_filament_id(self):
        with raises(ValidationError):
            CreateProjectRequestSchema(**valid_request_data(filament_id="invalid-uuid"))

    def test_server_controlled_fields(self):
        for field, value in [
            ("order_status", "delivered"),
            ("printer_id", "123e4567-e89b-12d3-a456-426614174000"),
            ("id", "123e4567-e89b-12d3-a456-426614174000")
        ]:
            with raises(ValidationError):
                CreateProjectRequestSchema(**valid_request_data(**{field: value}))
