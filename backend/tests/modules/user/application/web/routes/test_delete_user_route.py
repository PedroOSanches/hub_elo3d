from fastapi.testclient import TestClient

from src.app.app import app


class Test_DeleteUser:

    def test_delete_user(self):

        client = TestClient(app=app)

        deleted_user = client.delete(
        'user/delete_user/b189d11a-25d1-430e-b5a1-c53db528337e'
        )

        assert deleted_user.status_code == 200
        assert deleted_user.json()['name'] == 'User'
    
    def test_delete_user_not_found_user(self):

        client = TestClient(app=app)

        deleted_user = client.delete(
        'user/delete_user/b189d21a-25d1-430e-b5a1-c53db528337e'
        )


        assert deleted_user.status_code == 404
        assert deleted_user.json()['message'] == 'No users found for id: b189d21a-25d1-430e-b5a1-c53db528337e'

    def test_delete_user_type_id_invalid(self):

        client = TestClient(app)

        response = client.delete(
            "user/delete_user/1234"
        )

        assert response.status_code == 400
        assert response.json()['message'] == "The field 'id' has the wrong type. Received: str. Expected: UUID"