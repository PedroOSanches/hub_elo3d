from datetime import datetime, date
from uuid import uuid7
from fastapi import FastAPI
from fastapi.testclient import TestClient
from pytest import fixture

from src.shared.errors.base_error import BaseError
from src.shared.web.error_handlers import base_error_handler

from src.modules.project.application.controllers.update_project_controller import UpdateProjectController
from src.modules.project.application.usecases.update_project_usecase import UpdateProjectUsecase
from src.modules.project.application.web.routes.update_project import get_update_project_dependencies, get_current_user
from src.modules.project.application.web.routes.index import project_router
from src.modules.project.domain.entities.project import Project
from src.modules.project.domain.entities.project_file import ProjectFile
from src.modules.project.infra.repositories.project_repository_mock import ProjectRepositoryMock
from src.modules.user.domain.enums.role_enum import ROLE

@fixture
def valid_project():
    return Project(
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
        ]
    )

@fixture
def client_and_repo():
    app = FastAPI()
    app.include_router(project_router, prefix="/projects")
    app.add_exception_handler(BaseError, base_error_handler)

    repo = ProjectRepositoryMock()
    usecase = UpdateProjectUsecase(repo)
    controller = UpdateProjectController(usecase)

    app.dependency_overrides[get_update_project_dependencies] = lambda: controller
    app.dependency_overrides[get_current_user] = lambda: ROLE.HOSPITAL

    with TestClient(app) as client:
        yield client, repo

    app.dependency_overrides.clear()

class TestUpdateProjectRoute:
    def test_update_title(self, client_and_repo, valid_project):
        client, repo = client_and_repo
        repo.create_project(valid_project)

        response = client.patch(f"/projects/update/{valid_project.id}", json={"title": "Nova Prótese de mão"})

        assert response.status_code == 200
        assert response.json()["title"] == "Nova Prótese de mão"
        assert repo.get_project(valid_project.id).title == "Nova Prótese de mão"

    def test_update_status(self, client_and_repo, valid_project):
        client, repo = client_and_repo
        repo.create_project(valid_project)

        response = client.patch(f"/projects/update/{valid_project.id}", json={"new_status": "received"})

        assert response.status_code == 200

        history = response.json()["order_status"]

        assert "waiting_for_partner" in history
        assert "received" in history
        assert len(history) == 2
        assert datetime.fromisoformat(history["received"]).tzinfo is not None

    def test_invalid_transition(self, client_and_repo, valid_project):
        client, repo = client_and_repo
        repo.create_project(valid_project)

        response = client.patch(f"/projects/update/{valid_project.id}", json={"new_status": "delivered"})

        assert response.status_code == 409
        assert len(repo.get_project(valid_project.id).order_status) == 1

    def test_invalid_request(self, client_and_repo, valid_project):
        client, repo = client_and_repo
        repo.create_project(valid_project)

        response = client.patch(f"/projects/update/{valid_project.id}", json={"pieces_quantity": -5})

        assert response.status_code == 422
        assert repo.get_project(valid_project.id).pieces_quantity == 1

    def test_project_not_found(self, client_and_repo):
        client, _ = client_and_repo
        project_id = uuid7()

        response = client.patch(f"/projects/update/{project_id}", json={"title": "Novo título"})

        assert response.status_code == 404
        assert str(project_id) in response.json()["message"]

    def test_invalid_project_id(self, client_and_repo):
        client, _ = client_and_repo

        response = client.patch(f"/projects/update/invalid-uuid", json={"title": "Novo título"})

        assert response.status_code == 422

    def test_empty_request_body(self, client_and_repo, valid_project):
        client, repo = client_and_repo
        repo.create_project(valid_project)

        response = client.patch(f"/projects/update/{valid_project.id}", json={})

        assert response.status_code == 422

    def test_duplicate_status_returns_conflict(self, client_and_repo, valid_project):
        client, repo = client_and_repo
        repo.create_project(valid_project)

        response = client.patch(f"/projects/update/{valid_project.id}", json={"new_status": "waiting_for_partner"})

        assert response.status_code == 409
        assert len(repo.get_project(valid_project.id).order_status) == 1