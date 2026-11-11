from datetime import datetime, date, timedelta, timezone
from uuid import uuid7
import jwt
from fastapi.testclient import TestClient
from pytest import fixture

from src.app.app import app
from src.shared.environments.environments import env
from src.modules.project.application.web import dependencies as project_dependencies
from src.modules.project.domain.entities.project import Project
from src.modules.project.domain.entities.project_file import ProjectFile
from src.modules.project.infra.repositories.project_repository_mock import ProjectRepositoryMock

def make_access_token(role: str) -> str:
    payload = {
        "sub": str(uuid7()),
        "type": "access",
        "role": role,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=30)
    }

    return jwt.encode(payload, env.jwt_secret, algorithm="HS256")

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
def access_token():
    return make_access_token("hospital")

@fixture
def client_and_repo(monkeypatch, access_token):
    repo = ProjectRepositoryMock()

    monkeypatch.setattr(project_dependencies, "_project_repository", repo)

    with TestClient(app) as client:
        client.cookies.set("access_token", access_token)
        yield client, repo

class TestUpdateProjectIntegration:
    def test_update_project_success(self, client_and_repo, valid_project):
        client, repo = client_and_repo
        repo.create_project(valid_project)

        response = client.patch(f"/api/projects/update/{valid_project.id}", json={
            "title": "Prótese de mão atualizada"}
        )

        assert response.status_code == 200

        data = response.json()

        assert data["id"] == str(valid_project.id)
        assert data["title"] == "Prótese de mão atualizada"
        assert repo.get_project(valid_project.id).title == "Prótese de mão atualizada"

    def test_update_status_history(self, client_and_repo, valid_project):
        client, repo = client_and_repo
        repo.create_project(valid_project)

        response = client.patch(f"/api/projects/update/{valid_project.id}", json={
            "new_status": "received"}
        )

        assert response.status_code == 200

        history = response.json()["order_status"]

        assert "waiting_for_partner" in history
        assert "received" in history
        assert len(history) == 2

        timestamp = history["received"]

        assert datetime.fromisoformat(timestamp).tzinfo is not None

    def test_invalid_status_transition(self, client_and_repo, valid_project):
        client, repo = client_and_repo
        repo.create_project(valid_project)

        response = client.patch(f"/api/projects/update/{valid_project.id}", json={
            "new_status": "delivered"}
        )

        assert response.status_code == 409
        assert len(repo.get_project(valid_project.id).order_status) == 1

    def test_project_not_found(self, client_and_repo):
        client, _ = client_and_repo
        project_id = uuid7()

        response = client.patch(f"/api/projects/update/{project_id}", json={
            "title": "Projeto atualizado"}
        )

        assert response.status_code == 404

    def test_update_without_authentication(self, client_and_repo, valid_project):
        with TestClient(app) as client:
            response = client.patch(f"/api/projects/update/{valid_project.id}", json={
                "title": "Tentativa de atualização sem autenticação"}
            )

        assert response.status_code == 401
        assert response.json().get("message")

    def test_update_with_invalid_token(self, client_and_repo, valid_project):
        with TestClient(app) as client:
            client.cookies.set("access_token", "invalid_token")
            response = client.patch(f"/api/projects/update/{valid_project.id}", json={
                "title": "Tentativa de atualização com token inválido"}
            )

        assert response.status_code == 401
        assert response.json().get("message")

    def test_user_can_update_status(self, client_and_repo, valid_project):
        client, repo = client_and_repo
        repo.create_project(valid_project)

        client.cookies.set("access_token", make_access_token("user"))

        response = client.patch(f"/api/projects/update/{valid_project.id}", json={"new_status": "received"})

        assert response.status_code == 200
        assert "received" in response.json()["order_status"]

    def test_user_cannot_update_data(self, client_and_repo, valid_project):
        client, repo = client_and_repo
        repo.create_project(valid_project)

        client.cookies.set("access_token", make_access_token("user"))

        response = client.patch(f"/api/projects/update/{valid_project.id}", json={"title": "Novo título"})

        assert response.status_code == 403
        assert repo.get_project(valid_project.id).title == "Prótese de mão"

    def test_user_cannot_update_data_and_status(self, client_and_repo, valid_project):
        client, repo = client_and_repo
        repo.create_project(valid_project)

        client.cookies.set("access_token", make_access_token("user"))

        response = client.patch(f"/api/projects/update/{valid_project.id}", json={
            "title": "Novo título",
            "new_status": "received"
        })

        assert response.status_code == 403
        assert repo.get_project(valid_project.id).title == "Prótese de mão"
        assert len(repo.get_project(valid_project.id).order_status) == 1

    def test_user_hospital_can_update_data_and_status(self, client_and_repo, valid_project):
        client, repo = client_and_repo
        repo.create_project(valid_project)

        client.cookies.set("access_token", make_access_token("user_hospital"))

        response = client.patch(f"/api/projects/update/{valid_project.id}", json={
            "title": "Novo título",
            "new_status": "received"
        })

        assert response.status_code == 200
        assert response.json()["title"] == "Novo título"
        assert "received" in response.json()["order_status"]

    def test_admin_cannot_edit_project(self, client_and_repo, valid_project):
        client, repo = client_and_repo
        repo.create_project(valid_project)

        client.cookies.set("access_token", make_access_token("admin"))

        response = client.patch(f"/api/projects/update/{valid_project.id}", json={
            "title": "Novo título"
        })

        assert response.status_code == 403
        assert repo.get_project(valid_project.id).title == "Prótese de mão"

    def test_admin_cannot_update_status(self, client_and_repo, valid_project):
        client, repo = client_and_repo
        repo.create_project(valid_project)

        client.cookies.set("access_token", make_access_token("admin"))

        response = client.patch(f"/api/projects/update/{valid_project.id}", json={
            "new_status": "received"
        })

        assert response.status_code == 403
        assert len(repo.get_project(valid_project.id).order_status) == 1