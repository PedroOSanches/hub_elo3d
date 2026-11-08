from uuid import UUID, uuid4
from datetime import date, datetime, timezone

import pytest
from pydantic import ValidationError

from src.modules.project.domain.entities.project import Project
from src.modules.project.domain.enums.order_status_enum import OrderStatus
from src.modules.project.domain.enums.urgency_enum import Urgency
from src.modules.project.domain.enums.category_enum import Category
from src.modules.project.domain.entities.project_file import ProjectFile
from src.modules.project.domain.errors.project_errors import ProjectStatusConflictError

def valid_project_data(**overrides):
    data = {
        "title": "Prótese de mão",
        "date_end": date(2026, 11, 15),
        "urgency": Urgency.HIGH,
        "pieces_quantity": 2,
        "category": Category.PROSTHESIS,
        "description": "Prótese de mão para paciente em recuperação",
        "filament_id": UUID("123e4567-e89b-12d3-a456-426614174000"),
        "files": [
            ProjectFile(
                title = "Modelo de prótese",
                file_url = "https://example.com/protese.stl"
            )
        ]
    }
    data.update(overrides)
    return data

class TestProject:

    def test_create_project(self):
        project = Project(**valid_project_data())

        assert isinstance(project.id, UUID)
        assert project.title == "Prótese de mão"
        assert project.pieces_quantity == 2
        assert project.category == Category.PROSTHESIS
        assert project.technical_info is None
        assert OrderStatus.WAITING_FOR_PARTNER in project.order_status

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

    def test_custom_order_status(self):
        timestamp = datetime.now(timezone.utc)

        project = Project(**valid_project_data(order_status = {OrderStatus.RECEIVED: timestamp}))

        assert project.order_status[OrderStatus.RECEIVED] == timestamp

    def test_invalid_urgency(self):
        with pytest.raises(ValidationError):
            Project(**valid_project_data(urgency = "critical"))

    def test_invalid_order_status(self):
        with pytest.raises(ValidationError):
            Project(**valid_project_data(order_status = {"invalid_status": datetime.now(timezone.utc)}))

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

    def test_project_with_one_file(self):
        project = Project(**valid_project_data())

        assert len(project.files) == 1
        assert isinstance(project.files[0], ProjectFile)

    def test_project_with_multiple_files(self):
        files = [
            ProjectFile(title = "Modelo de prótese", file_url = "https://example.com/protese.stl"),
            ProjectFile(title = "Manual do usuário", file_url = "https://example.com/manual.pdf")
        ]
        project = Project(**valid_project_data(files = files))

        assert len(project.files) == 2
        assert project.files[0].title == "Modelo de prótese"
        assert project.files[1].title == "Manual do usuário"

    def test_required_files(self):
        data = valid_project_data()
        data.pop("files")

        with pytest.raises(ValidationError):
            Project(**data)

    def test_empty_files_list(self):
        with pytest.raises(ValidationError):
            Project(**valid_project_data(files = []))

    def test_invalid_file(self):
        with pytest.raises(ValidationError):
            Project(**valid_project_data(files = {"title": "Modelo inválido"}))
    
    @pytest.mark.parametrize(
        "category",
        [
            Category.ORTHOSIS,
            Category.PROSTHESIS,
            Category.ACCESSORY,
            Category.ADAPTER,
            Category.OTHER,
        ],
    )
    def test_valid_categories(self, category):
        project = Project(**valid_project_data(category=category))

        assert project.category == category

    def test_invalid_category(self):
        with pytest.raises(ValidationError):
            Project(**valid_project_data(category="Ortopedia"))

    def test_project_generates_uuid7(self):
        project = Project(**valid_project_data())

        assert isinstance(project.id, UUID)
        assert project.id.version == 7

    @pytest.mark.parametrize(
        "status",
        [
            OrderStatus.WAITING_FOR_PARTNER,
            OrderStatus.RECEIVED,
            OrderStatus.IN_PROGRESS,
            OrderStatus.FINALIZED,
            OrderStatus.DELIVERED,
        ],
    )
    def test_valid_order_status(self, status):
        timestamp = datetime.now(timezone.utc)

        project = Project(**valid_project_data(order_status={status: timestamp}))

        assert project.order_status[status] == timestamp

    def test_removed_production_status_is_invalid(self):
        with pytest.raises(ValidationError):
            Project(**valid_project_data(production_status="received"))

    def test_initial_order_status_timestamp(self):
        project = Project(**valid_project_data())
        timestamp = project.order_status[OrderStatus.WAITING_FOR_PARTNER]

        assert isinstance(timestamp, datetime)
        assert timestamp.utcoffset().total_seconds() == 0

    def test_order_status_serialization(self):
        project = Project(**valid_project_data())
        data = project.model_dump(mode="json")

        assert "waiting_for_partner" in data["order_status"]

        timestamp = data["order_status"]["waiting_for_partner"]

        assert datetime.fromisoformat(timestamp).tzinfo is not None

    def test_independent_order_status_timestamps(self):
        project1 = Project(**valid_project_data())
        project2 = Project(**valid_project_data())

        assert project1.order_status is not project2.order_status

    def test_register_order_status(self):
        project = Project(**valid_project_data())

        initial_timestamp = project.order_status[OrderStatus.WAITING_FOR_PARTNER]
        project.register_order_status(OrderStatus.RECEIVED)

        assert len(project.order_status) == 2
        assert project.order_status[OrderStatus.WAITING_FOR_PARTNER] == initial_timestamp

        received_timestamp = project.order_status[OrderStatus.RECEIVED]

        assert isinstance(received_timestamp, datetime)
        assert received_timestamp.utcoffset().total_seconds() == 0
        assert received_timestamp >= initial_timestamp

    def test_register_multiple_order_statuses(self):
        project = Project(**valid_project_data())

        project.register_order_status(OrderStatus.RECEIVED)
        project.register_order_status(OrderStatus.IN_PROGRESS)

        assert len(project.order_status) == 3
        assert OrderStatus.RECEIVED in project.order_status
        assert OrderStatus.IN_PROGRESS in project.order_status

    def test_cannot_register_duplicate_order_status(self):
        project = Project(**valid_project_data())

        project.register_order_status(OrderStatus.RECEIVED)
        original_timestamp = project.order_status[OrderStatus.RECEIVED]

        with pytest.raises(ValueError):
            project.register_order_status(OrderStatus.RECEIVED)

        assert project.order_status[OrderStatus.RECEIVED] == original_timestamp

    def test_cannot_register_invalid_order_status(self):
        project = Project(**valid_project_data())

        with pytest.raises(ValueError):
            project.register_order_status("invalid_status")

        assert len(project.order_status) == 1

    def test_registered_status_serialization(self):
        project = Project(**valid_project_data())

        project.register_order_status(OrderStatus.RECEIVED)

        data = project.model_dump(mode="json")

        assert "waiting_for_partner" in data["order_status"]
        assert "received" in data["order_status"]

        timestamp = data["order_status"]["received"]

        assert datetime.fromisoformat(timestamp).tzinfo is not None

    def test_current_order_status_initial(self):
        project = Project(**valid_project_data())

        assert project.current_order_status == OrderStatus.WAITING_FOR_PARTNER

    def test_current_order_status_after_registration(self):
        project = Project(**valid_project_data())

        project.register_order_status(OrderStatus.RECEIVED)
        project.register_order_status(OrderStatus.IN_PROGRESS)

        assert project.current_order_status == OrderStatus.IN_PROGRESS

    def test_current_order_status_with_no_statuses(self):
        project = Project(**valid_project_data())
        project.order_status.clear()

        with pytest.raises(ValueError):
            _ = project.current_order_status

    def test_filament_id_is_required(self):
        with pytest.raises(ValidationError):
            Project(**valid_project_data(filament_id=None))

    def test_cannot_skip_order_status(self):
        project = Project(**valid_project_data())
        original_history = project.order_status.copy()

        with pytest.raises(ValueError, match="Status inválido"):
            project.register_order_status(OrderStatus.IN_PROGRESS)

        assert project.order_status == original_history

    def test_complete_order_status_flow(self):
        project = Project(**valid_project_data())

        statuses = [
            OrderStatus.RECEIVED,
            OrderStatus.IN_PROGRESS,
            OrderStatus.FINALIZED,
            OrderStatus.DELIVERED
        ]

        for status in statuses:
            project.register_order_status(status)

            assert project.current_order_status == status

        assert len(project.order_status) == 5

    def test_invalid_transition_raises_especific_error(self):
        project = Project(**valid_project_data())

        with pytest.raises(ProjectStatusConflictError, match="Status inválido"):
            project.register_order_status(OrderStatus.IN_PROGRESS)

    def test_duplicate_status_raises_especific_error(self):
        project = Project(**valid_project_data())

        with pytest.raises(ProjectStatusConflictError, match="Status já registrado"):
            project.register_order_status(OrderStatus.WAITING_FOR_PARTNER)