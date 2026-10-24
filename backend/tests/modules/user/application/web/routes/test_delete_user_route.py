from fastapi.testclient import TestClient

from src.app.app import app


class Test_DeleteUser:

    def test_delete_user(self):

        client = TestClient(app=app)

        deleted_user = client.delete(
        'user/delete_user/0334c795-5e71-4c1e-8a0e-ab21a4fcdecf'
        )

        assert deleted_user.status_code == 200
        assert deleted_user.json()['name'] == 'User'
