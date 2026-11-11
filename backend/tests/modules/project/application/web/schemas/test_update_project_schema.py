from datetime import datetime, date
from uuid import uuid7
from pytest import mark, raises
from pydantic import ValidationError

from src.modules.project.application.web.schemas.update_project_schema import UpdateProjectRequestSchema, UpdateProjectResponseSchema
from src.modules.project.domain.entities.project import Project
from src.modules.project.domain.entities.project_file import ProjectFile
from src.modules.project.domain.enums.order_status_enum import OrderStatus

class TestUpdateProjectRequestSchema:
    def test_partial_update(self):
        request = UpdateProjectRequestSchema(
            title="Updated Title"
        )

        changes = request.model_dump(exclude_unset=True, exclude={"new_status"})

        assert changes == {"title": "Updated Title"}

    def test_status_only_update(self):
        request = UpdateProjectRequestSchema(
            new_status="received"
        )

        assert request.new_status == OrderStatus.RECEIVED

    def test_nullable_fields_can_be_cleared(self):
        request = UpdateProjectRequestSchema(
            technical_info=None
        )

        changes = request.model_dump(exclude_unset=True)

        assert "technical_info" in changes
        assert changes["technical_info"] is None

    def test_description_is_stripped(self):
        request = UpdateProjectRequestSchema(
            description="   Nova descrição   "
        )

        assert request.description == "Nova descrição"

    @mark.parametrize(
        "data",
        [
            {},
            {"title": None},
            {"title": "AB"},
            {"pieces_quantity": 0},
            {"description": "   "},
            {"category": "invalid_category"},
            {"new_status": "invalid_status"},
            {"filament_id": "invalid-uuid"},
            {"files": []},
            {"id": str(uuid7())},
            {"order_status": {}}
        ]
    )
    def test_invalid_request(self, data):
        with raises(ValidationError):
            UpdateProjectRequestSchema.model_validate(data)

    class TestUpdateProjectResponseSchema:
        def test_response_contains_status_history(self):
            project = Project(
                title="Prótese de mão",
                date_end=date(2026, 11, 15),
                pieces_quantity=1,
                category="prosthesis",
                description="Projeto para reabilitação",
                urgency="high",
                filament_id=uuid7(),
                files=[
                    ProjectFile(
                        title="Modelo 3D",
                        file_url="https://example.com/model.stl"
                    )
                ],
            )

            project.register_order_status(OrderStatus.RECEIVED)

            response = UpdateProjectResponseSchema.model_validate(project)
            data = response.model_dump(mode="json")
            history = data["order_status"]

            assert data["id"] == str(project.id)
            assert "waiting_for_partner" in history
            assert "received" in history

            for timestamp in history.values():
                assert datetime.fromisoformat(timestamp).tzinfo is not None