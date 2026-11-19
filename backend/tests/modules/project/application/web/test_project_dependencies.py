from pytest import mark

from src.modules.project.application.web.dependencies import (
    get_repo_project
)
from src.modules.project.infra.repositories.project_repository_neo import (
    ProjectRepositoryNeo
)
from src.modules.project.infra.repositories.project_repository_mock import (
    ProjectRepositoryMock
)
from src.shared.environments.environments import STAGE, env


@mark.parametrize(
    "stage",
    [
        STAGE.TEST,
        STAGE.DOTENV
    ]
)
def test_get_repo_project_uses_mock_outside_prod(stage, monkeypatch):
    monkeypatch.setattr(env, "stage", stage)

    repo = get_repo_project()

    assert isinstance(repo, ProjectRepositoryMock)

def test_get_repo_project_uses_neo4j_in_prod(monkeypatch):
    monkeypatch.setattr(env, "stage", STAGE.PROD)

    repo = get_repo_project()

    assert isinstance(repo, ProjectRepositoryNeo)