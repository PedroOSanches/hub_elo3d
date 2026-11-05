from datetime import date
from uuid import uuid4
from fastapi import FastAPI
from fastapi.testclient import TestClient
from pytest import fixture

from src.shared.errors.base_error import BaseError
from src.shared.web.error_handlers import base_error_handler

from src.modules.project.domain.entities.project import Project
from src.modules.project.domain.entities.project_file import ProjectFile
from src.modules.project.application.controllers.get_project_controller import GetProjectController
from src.modules.project.application.usecases.get_project_usecase import GetProjectUsecase
from src.modules.project.application.web.routes.get_project import get_get_project_dependencies
from src.modules.project.application.web.routes.index import project_router
from src.modules.project.infra.repositories.project_repository_mock import ProjectRepositoryMock

@fixture
def valid_project():
    return Project(
        id=uuid4(),
        title="Prótese de mão",
        date_end=date(2026, 11, 15),
        pieces_quantity=1,
        category="prosthesis",
        description="Projeto para reabilitação",
        technical_info=None,
        urgency="high",
        filament_id=uuid4(),
        files=[
            ProjectFile(
                title="Modelo 3D",
                file_url="https://example.com/model.stl",
            )
        ],
    )

@fixture
def client_and_repo():
    app = FastAPI()
    app.include_router(project_router, prefix="/projects")
    app.add_exception_handler(BaseError, base_error_handler)

    repo = ProjectRepositoryMock()
    usecase = GetProjectUsecase(repo)
    controller = GetProjectController(usecase)

    app.dependency_overrides[get_get_project_dependencies] = lambda: controller

    with TestClient(app) as client:
        yield client, repo

    app.dependency_overrides.clear()

class TestGetProjectRoute:
    def test_get_project_success(self, client_and_repo, valid_project):
        client, repo = client_and_repo
        repo.create_project(valid_project)

        response = client.get(f"/projects/get/{valid_project.id}")

        assert response.status_code == 200
        data = response.json()

        assert data["id"] == str(valid_project.id)
        assert data["title"] == valid_project.title
        assert data["order_status"] == "waiting_for_partner"

    def test_get_nonexistent_project(self, client_and_repo):
        client, _ = client_and_repo

        project_id = uuid4()

        response = client.get(f"/projects/get/{project_id}")

        assert response.status_code == 404
        assert str(project_id) in response.json()["message"]

    def test_get_project_invalid_id(self, client_and_repo):
        client, repo = client_and_repo

        response = client.get("/projects/get/invalid-uuid")

        assert response.status_code == 422
        assert len(repo.projects) == 0