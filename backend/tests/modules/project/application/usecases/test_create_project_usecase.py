from datetime import date
from unittest.mock import Mock
from uuid import uuid4

from pytest import raises
from pydantic import ValidationError

from src.modules.project.application.usecases.create_project_usecase import CreateProjectUsecase
from src.modules.project.domain.entities.project import Project
from src.modules.project.domain.entities.project_file import ProjectFile
from src.modules.project.domain.enums.order_status_enum import OrderStatus
from src.modules.project.domain.enums.urgency_enum import Urgency
from src.modules.project.domain.repositories.project_repository_interface import IProjectRepository

def valid_create_data(**overrides):
    data = {
        "title": "Prótese de mão",
        "date_end": date(2026, 11, 15),
        "pieces_quantity": 1,
        "category": "Ortopedia",
        "description": "Prótese de mão para paciente em recuperação",
        "urgency": Urgency.HIGH,
        "filament_id": uuid4(),
        "files": [ProjectFile(title = "Modelo 3D", file_url = "https://example.com/model.stl")]
    }
    data.update(overrides)
    return data

class TestCreateProjectUsecase:
    def test_create_project(self):
        repo = Mock(spec=IProjectRepository)
        repo.create_project.side_effect = lambda project: project

        usecase = CreateProjectUsecase(repo)
        
        project = usecase(**valid_create_data())

        assert isinstance(project, Project)
        assert project.pieces_quantity == 1
        assert project.category == "Ortopedia"
        assert project.order_status == OrderStatus.WAITING_FOR_PARTNER
        assert project.production_status is None
        assert project.printer_id is None

        repo.create_project.assert_called_once_with(project = project)

    def test_invalid_quantity_does_not_save(self):
        repo = Mock(spec=IProjectRepository)
        usecase = CreateProjectUsecase(repo)

        with raises(ValidationError):
            usecase(**valid_create_data(pieces_quantity = 0))

        repo.create_project.assert_not_called()

    def test_description_is_normalized(self):
        repo = Mock(spec=IProjectRepository)
        repo.create_project.side_effect = lambda project: project

        usecase = CreateProjectUsecase(repo)
        
        project = usecase(**valid_create_data(description = "   Prótese de mão para paciente em recuperação   "))

        assert project.description == "Prótese de mão para paciente em recuperação"