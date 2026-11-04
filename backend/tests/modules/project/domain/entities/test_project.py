from uuid import UUID, uuid4
from datetime import date

from pytest import fixture, raises, mark
from pydantic import ValidationError

from src.modules.project.domain.entities.project import Project
from src.modules.project.domain.enums.order_status_enum import OrderStatus
from src.modules.project.domain.enums.urgency_enum import Urgency
from src.modules.project.domain.enums.category_enum import Category
from src.modules.project.domain.entities.project_file import ProjectFile

@fixture
def valid_project_data():
    return {
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

class TestProject:

    def test_create_project(self, valid_project_data):
        project = Project(**valid_project_data)

        assert isinstance(project.id, UUID)
        assert project.title == "Prótese de mão"
        assert project.urgency == "high"
        assert project.pieces_quantity == 2
        assert project.category == Category.PROSTHESIS
        assert project.technical_info is None
        assert project.order_status == "waiting_for_partner"

    def test_different_ids(self, valid_project_data):
        project1 = Project(**valid_project_data)

        project2 = Project(**valid_project_data)

        assert project1.id != project2.id

    def test_required_title(self, valid_project_data):
        data = valid_project_data
        data.pop("title")

        with raises(ValidationError):
            Project(**data)

    def test_short_title(self, valid_project_data):
        data = {
            **valid_project_data,
            "title": "AB"
        }

        with raises(ValidationError):
            Project(**data)

    def test_required_date_end(self, valid_project_data):
        data = valid_project_data
        data.pop("date_end")

        with raises(ValidationError):
            Project(**data)

    def test_unknown_field(self, valid_project_data):
        data = valid_project_data
        data["unknown_field"] = "Teste"

        with raises(ValidationError):
            Project(**data)

    def test_required_urgency(self, valid_project_data):
        data = valid_project_data
        data.pop("urgency")

        with raises(ValidationError):
            Project(**data)

    def test_custom_order_status(self, valid_project_data):
        data = {
            **valid_project_data,
            "order_status": OrderStatus.IN_PROGRESS
        }
        project = Project(**data)

        assert project.order_status == "in_progress"
        assert type(project.order_status) is str

    def test_delivered_order_status(self, valid_project_data):
        data = {
            **valid_project_data,
            "order_status": OrderStatus.DELIVERED
        }
        project = Project(**data)

        assert project.order_status == "delivered"

    def test_invalid_urgency(self, valid_project_data):
        data = {
            **valid_project_data,
            "urgency": "critical"
        }

        with raises(ValidationError):
            Project(**data)

    def test_invalid_order_status(self, valid_project_data):
        data = {
            **valid_project_data,
            "order_status": "canceled"
        }

        with raises(ValidationError):
            Project(**data)

    def test_required_pieces_quantity(self, valid_project_data):
        data = valid_project_data
        data.pop("pieces_quantity")

        with raises(ValidationError):
            Project(**data)

    def test_invalid_pieces_quantity(self, valid_project_data):
        data = {
            **valid_project_data,
            "pieces_quantity": 0
        }

        with raises(ValidationError):
            Project(**data)

    def test_negative_pieces_quantity(self, valid_project_data):
        data = {
            **valid_project_data,
            "pieces_quantity": -5
        }

        with raises(ValidationError):
            Project(**data)

    def test_required_category(self, valid_project_data):
        data = valid_project_data
        data.pop("category")

        with raises(ValidationError):
            Project(**data)

    def test_empty_category(self, valid_project_data):
        data = {
            **valid_project_data,
            "category": ""
        }

        with raises(ValidationError):
            Project(**data)

    def test_required_description(self, valid_project_data):
        data = valid_project_data
        data.pop("description")

        with raises(ValidationError):
            Project(**data)

    def test_description_max_length(self, valid_project_data):
        data = {
            **valid_project_data,
            "description": "A" * 281
        }
        
        with raises(ValidationError):
            Project(**data)

    def test_description_only_spaces(self, valid_project_data):
        data = {
            **valid_project_data,
            "description": "   "
        }

        with raises(ValidationError):
            Project(**data)

    def test_description_removes_spaces(self, valid_project_data):
        data = {
            **valid_project_data,
            "description": "   Projeto de teste   "
        }

        project = Project(**data)

        assert project.description == "Projeto de teste"

    def test_description_only_line_breaks(self, valid_project_data):
        data = {
            **valid_project_data,
            "description": "\n\t  "
        }

        with raises(ValidationError):
            Project(**data)

    def test_optional_technical_info(self, valid_project_data):
        project = Project(**valid_project_data)

        assert project.technical_info is None

    def test_with_technical_info(self, valid_project_data):
        data = {
            **valid_project_data,
            "technical_info": "Impressão com 30% de preenchimento"
        }

        project = Project(**data)

        assert project.technical_info == "Impressão com 30% de preenchimento"

    def test_printer_id_optional(self, valid_project_data):
        project = Project(**valid_project_data)

        assert project.printer_id is None

    def test_project_with_printer_id(self, valid_project_data):
        printer_id = uuid4()
        data = {
            **valid_project_data,
            "printer_id": printer_id
        }
        project = Project(**data)

        assert project.printer_id == printer_id

    def test_invalid_printer_id(self, valid_project_data):
        data = {
            **valid_project_data,
            "printer_id": "invalid-uuid"
        }

        with raises(ValidationError):
            Project(**data)

    def test_project_with_filament_id(self, valid_project_data):
        filament_id = uuid4()
        data = {
            **valid_project_data,
            "filament_id": filament_id
        }
        project = Project(**data)

        assert project.filament_id == filament_id

    def test_required_filament_id(self, valid_project_data):
        data = valid_project_data
        data.pop("filament_id")

        with raises(ValidationError):
            Project(**data)

    def test_invalid_filament_id(self, valid_project_data):
        data = {
            **valid_project_data,
            "filament_id": "invalid-uuid"
        }

        with raises(ValidationError):
            Project(**data)

    def test_project_with_one_file(self, valid_project_data):
        project = Project(**valid_project_data)

        assert len(project.files) == 1
        assert isinstance(project.files[0], ProjectFile)

    def test_project_with_multiple_files(self, valid_project_data):
        files = [
            ProjectFile(title = "Modelo de prótese", file_url = "https://example.com/protese.stl"),
            ProjectFile(title = "Manual do usuário", file_url = "https://example.com/manual.pdf")
        ]
        data = {
            **valid_project_data,
            "files": files
        }
        project = Project(**data)

        assert len(project.files) == 2
        assert project.files[0].title == "Modelo de prótese"
        assert project.files[1].title == "Manual do usuário"

    def test_required_files(self, valid_project_data):
        data = valid_project_data
        data.pop("files")

        with raises(ValidationError):
            Project(**data)

    def test_empty_files_list(self, valid_project_data):
        data = {
            **valid_project_data,
            "files": []
        }

        with raises(ValidationError):
            Project(**data)

    def test_invalid_file(self, valid_project_data):
        data = {
            **valid_project_data,
            "files": [{"title": "Modelo inválido"}]
        }

        with raises(ValidationError):
            Project(**data)

    def test_enum_values(self, valid_project_data):
        data = {
            **valid_project_data,
            "urgency": Urgency.HIGH,
            "order_status": OrderStatus.RECEIVED
        }

        project = Project(**data)

        assert project.urgency == "high"
        assert project.order_status == "received"

        assert type(project.urgency) is str
        assert type(project.order_status) is str
    
    @mark.parametrize("status", [
        OrderStatus.WAITING_FOR_PARTNER,
        OrderStatus.RECEIVED,
        OrderStatus.IN_PROGRESS,
        OrderStatus.FINALIZED,
        OrderStatus.DELIVERED
    ])

    def test_valid_order_status(self, status, valid_project_data):
        data = {
            **valid_project_data,
            "order_status": status
        }

        project = Project(**data)

        assert project.order_status == status.value
        assert type(project.order_status) is str

    def test_default_order_status(self, valid_project_data):
        project = Project(**valid_project_data)

        assert project.order_status == "waiting_for_partner"
        assert type(project.order_status) is str

    def test_enum_values_serialization(self, valid_project_data):
        project = Project(**valid_project_data)
        data = project.model_dump()

        assert data["order_status"] == "waiting_for_partner"
        assert data["urgency"] == "high"

    def test_removed_status_is_invalid(self, valid_project_data):
        data = {
            **valid_project_data,
            "order_status": "completed"
        }

        with raises(ValidationError):
            Project(**data)

    @mark.parametrize(
        "category",
        [
            Category.ORTHOSIS,
            Category.PROSTHESIS,
            Category.ACCESSORY,
            Category.ADAPTER,
            Category.OTHER,
        ],
    )
    def test_valid_categories(self, category, valid_project_data):
        data = {
            **valid_project_data,
            "category": category,
        }

        project = Project(**data)

        assert project.category == category

    def test_invalid_category(self, valid_project_data):
        data = {
            **valid_project_data,
            "category": "Ortopedia",
        }

        with raises(ValidationError):
            Project(**data)
    
    def test_filament_id_cannot_be_none(self, valid_project_data):
        data = {
            **valid_project_data,
            "filament_id": None,
        }

        with raises(ValidationError):
            Project(**data)