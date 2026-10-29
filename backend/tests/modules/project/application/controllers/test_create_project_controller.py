import json
from datetime import date
from unittest.mock import Mock
from uuid import UUID, uuid4

from src.modules.project.application.controllers.create_project_controller import CreateProjectController
from src.modules.project.application.usecases.create_project_usecase import CreateProjectUsecase
from src.modules.project.application.web.schemas.create_project_schema import CreateProjectRequestSchema
from src.modules.project.domain.entities.project import Project
from src.modules.project.domain.repositories.project_repository_interface import IProjectRepository

def valid_request_data(**overrides):
    data = {
        "title": "Prótese de mão",
        "date_end": "2026-11-15",
        "pieces_quantity": 1,
        "category": "Ortopedia",
        "description": "Prótese para reabilitação",
        "urgency": "high",
        "filament_id": str(uuid4()),
        "files": [
            {
                "title": "Modelo 3D",
                "file_url": "https://example.com/model.stl"
            }
        ]
    }

    data.update(overrides)
    return data

class TestCreateProjectController:
    def test_create_project_controller(self):
        repo = Mock(spec=IProjectRepository)
        repo.create_project.side_effect = lambda project: project

        usecase = CreateProjectUsecase(repo)
        controller = CreateProjectController(usecase)

        request = CreateProjectRequestSchema(**valid_request_data())
        response = controller(request)

        assert isinstance(response, dict)
        assert response["title"] == "Prótese de mão"
        assert response["pieces_quantity"] == 1
        assert response["order_status"] == "waiting_for_partner"
        assert response["urgency"] == "high"
        assert response["printer_id"] is None
        assert response["date_end"] == "2026-11-15"
        assert response["files"][0]["title"] == "Modelo 3D"
        assert UUID(response["id"])

        json.dumps(response)

        repo.create_project.assert_called_once()

    def test_controller_sends_project_to_repository(self):
        repo = Mock(spec=IProjectRepository)
        repo.create_project.side_effect = lambda project: project

        controller = CreateProjectController(CreateProjectUsecase(repo))
        request = CreateProjectRequestSchema(**valid_request_data())
        controller(request)

        saved_project = repo.create_project.call_args.kwargs["project"]

        assert isinstance(saved_project, Project)
        assert saved_project.title == request.title
        assert saved_project.pieces_quantity == request.pieces_quantity
        assert saved_project.order_status == "waiting_for_partner"

    def test_controller_with_technical_info(self):
        repo = Mock(spec=IProjectRepository)
        repo.create_project.side_effect = lambda project: project

        controller = CreateProjectController(CreateProjectUsecase(repo))
        request = CreateProjectRequestSchema(**valid_request_data(technical_info="Preenchimento de 30%"))
        response = controller(request)

        assert response["technical_info"] == "Preenchimento de 30%"