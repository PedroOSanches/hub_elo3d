from datetime import UTC, datetime, timedelta
from uuid import uuid4

import jwt
import pytest
from fastapi.testclient import TestClient

from src.app.app import app
from src.shared.environments.environments import env


@pytest.fixture
def access_token():
    payload = {
        "sub": str(uuid4()),
        "type": "access",
        "exp": datetime.now(UTC) + timedelta(minutes=30)
    }
    
    return jwt.encode(payload, env.jwt_secret, algorithm="HS256")

@pytest.fixture
def client(access_token):
    client = TestClient(app=app)
    client.cookies.set('access_token', access_token)

    return client

def test_generate_upload_url(client: TestClient):

    response = client.post(
        '/api/projects/upload/generate_upload_url',
        json={
            "files": [
                {
                    "file_name": "test_model",
                    "size": 1500,
                    "content_type": "application/pdf",
                    }
                ]
            }
    ).json()

    assert response[-1]['object_key'] is not None
    assert response[-1]['upload_url'] is not None

    
def test_generate_upload_url_mime_type_invalid(client: TestClient):

    response = client.post(
        '/api/projects/upload/generate_upload_url',
        json={
            "files": [
                {
                    "file_name": "test_model",
                    "size": 1500,
                    "content_type": "a/a",
                    }
                ]
            }
    ).json()

    assert response['message'] == (
        "The field 'content_type' has the wrong type. "
        "Received: str. "
        "Expected: <enum 'ContentTypeEnum'>"
    )

