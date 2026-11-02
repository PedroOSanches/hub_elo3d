from pytest import fixture
from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.modules.project.application.controllers.create_project_controller import CreateProjectController
from src.modules.project.application.usecases.create_project_usecase import CreateProjectUsecase
from src.modules.project.application.web.routes.create_project import get_create_project_dependencies
from src.modules.project.application.web.routes.index import project_router
from src.modules.project.infra.repositories.project_repository_mock import ProjectRepositoryMock

def valid_request_data(**overrides):
    data = {
        "title": "Prótese de mão",
        "date_end": "2026-11-15",
        "pieces_quantity": 1,
        "category": "Ortopedia",
        "description": "Prótese para reabilitação",
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

@fixture
def client_and_repo():
    app = FastAPI()
    app.include_router(
        project_router,
        prefix="/projects"
    )

    repo = ProjectRepositoryMock()
    usecase = CreateProjectUsecase(repo)
    controller = CreateProjectController(usecase)

    app.dependency_overrides[get_create_project_dependencies] = lambda: controller

    with TestClient(app) as client:
        yield client, repo

    app.dependency_overrides.clear()

class TestCreateProjectRoute:
    def test_create_project_success(self, client_and_repo):
        client, repo = client_and_repo
        response = client.post(
            "/projects/create",
            json=valid_request_data()
        )

        assert response.status_code == 201

        data = response.json()

        assert data["title"] == "Prótese de mão"
        assert data["date_end"] == "2026-11-15"
        assert data["pieces_quantity"] == 1
        assert len(repo.projects) == 1

    def test_invalid_quantity(self, client_and_repo):
        client, repo = client_and_repo
        response = client.post(
            "/projects/create",
            json=valid_request_data(pieces_quantity=0)
        )

        assert response.status_code == 422
        assert len(repo.projects) == 0

    def test_required_files(self, client_and_repo):
        client, repo = client_and_repo
        response = client.post(
            "/projects/create",
            json=valid_request_data(files=[])
        )

        assert response.status_code == 422
        assert len(repo.projects) == 0

    def test_cannot_define_order_status(self, client_and_repo):
        client, repo = client_and_repo
        response = client.post(
            "/projects/create",
            json=valid_request_data(order_status="completed")
        )

        assert response.status_code == 422
        assert len(repo.projects) == 0