from uuid import UUID, uuid4
from datetime import date

import pytest
from pydantic import ValidationError

from src.modules.project.domain.entities.project import Project
from src.modules.project.domain.enums.order_status_enum import OrderStatus
from src.modules.project.domain.enums.production_status_enum import ProductionStatus
from src.modules.project.domain.enums.urgency_enum import Urgency

def valid_project_data(**overrides):
    data = {
        "title": "Prótese de mão",
        "date_end": date(2026, 11, 15),
        "urgency": Urgency.HIGH,
        "pieces_quantity": 2,
        "category": "Ortopedia",
        "description": "Prótese de mão para paciente em recuperação",
        "filament_id": UUID("123e4567-e89b-12d3-a456-426614174000")
    }
    data.update(overrides)
    return data

class TestProject:

    def test_create_project(self):
        project = Project(**valid_project_data())

        assert isinstance(project.id, UUID)
        assert project.title == "Prótese de mão"
        assert project.pieces_quantity == 2
        assert project.category == "Ortopedia"
        assert project.technical_info is None
        assert project.order_status == OrderStatus.WAITING_FOR_PARTNER

    def test_different_ids(self):
        project1 = Project(**valid_project_data())

        project2 = Project(**valid_project_data())

        assert project1.id != project2.id

    def test_required_title(self):
        data = valid_project_data()
        data.pop("title")

        with pytest.raises(ValidationError):
            Project(**data)

    def test_short_title(self):
        with pytest.raises(ValidationError):
            Project(**valid_project_data(title = "AB"))

    def test_required_date_end(self):
        data = valid_project_data()
        data.pop("date_end")

        with pytest.raises(ValidationError):
            Project(**data)

    def test_unknown_field(self):
        data = valid_project_data()
        data["unknown_field"] = "Teste"

        with pytest.raises(ValidationError):
            Project(**data)

    def test_required_urgency(self):
        data = valid_project_data()
        data.pop("urgency")

        with pytest.raises(ValidationError):
            Project(**data)

    def test_production_status(self):
        project = Project(**valid_project_data(production_status = ProductionStatus.IN_PRODUCTION))

        assert project.production_status == ProductionStatus.IN_PRODUCTION

    def test_custom_order_status(self):
        project = Project(**valid_project_data(order_status = OrderStatus.IN_PROGRESS))

        assert project.order_status == OrderStatus.IN_PROGRESS

    def test_invalid_urgency(self):
        with pytest.raises(ValidationError):
            Project(**valid_project_data(urgency = "critical"))

    def test_invalid_order_status(self):
        with pytest.raises(ValidationError):
            Project(**valid_project_data(order_status = "canceled"))

    def test_invalid_production_status(self):
        with pytest.raises(ValidationError):
            Project(**valid_project_data(production_status = "printing_error"))

    def test_required_pieces_quantity(self):
        data = valid_project_data()
        data.pop("pieces_quantity")

        with pytest.raises(ValidationError):
            Project(**data)

    def test_invalid_pieces_quantity(self):
        with pytest.raises(ValidationError):
            Project(**valid_project_data(pieces_quantity = 0))

    def test_negative_pieces_quantity(self):
        with pytest.raises(ValidationError):
            Project(**valid_project_data(pieces_quantity = -5))

    def test_required_category(self):
        data = valid_project_data()
        data.pop("category")

        with pytest.raises(ValidationError):
            Project(**data)

    def test_empty_category(self):
        with pytest.raises(ValidationError):
            Project(**valid_project_data(category = ""))

    def test_required_description(self):
        data = valid_project_data()
        data.pop("description")

        with pytest.raises(ValidationError):
            Project(**data)

    def test_description_max_length(self):
        with pytest.raises(ValidationError):
            Project(**valid_project_data(description = "A" * 281))

    def test_description_only_spaces(self):
        with pytest.raises(ValidationError):
            Project(**valid_project_data(description = "   "))

    def test_description_removes_spaces(self):
        project = Project(**valid_project_data(description = "   Projeto de teste   "))

        assert project.description == "Projeto de teste"

    def test_description_only_line_breaks(self):
        with pytest.raises(ValidationError):
            Project(**valid_project_data(description = "\n\t  "))

    def test_optional_technical_info(self):
        project = Project(**valid_project_data())

        assert project.technical_info is None

    def test_with_technical_info(self):
        project = Project(**valid_project_data(technical_info = "Impressão com 30% de preenchimento"))

        assert project.technical_info == "Impressão com 30% de preenchimento"

    def test_printer_id_optional(self):
        project = Project(**valid_project_data())

        assert project.printer_id is None

    def test_project_with_printer_id(self):
        printer_id = uuid4()
        project = Project(**valid_project_data(printer_id = printer_id))

        assert project.printer_id == printer_id

    def test_invalid_printer_id(self):
        with pytest.raises(ValidationError):
            Project(**valid_project_data(printer_id = "invalid-uuid"))

    def test_project_with_filament_id(self):
        filament_id = uuid4()
        project = Project(**valid_project_data(filament_id = filament_id))

        assert project.filament_id == filament_id

    def test_required_filament_id(self):
        data = valid_project_data()
        data.pop("filament_id")

        with pytest.raises(ValidationError):
            Project(**data)

    def test_invalid_filament_id(self):
        with pytest.raises(ValidationError):
            Project(**valid_project_data(filament_id = "invalid-uuid"))