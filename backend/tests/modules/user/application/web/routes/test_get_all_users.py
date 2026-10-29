from fastapi.testclient import TestClient

from src.app.app import app
from src.modules.user.application.web.routes.get_all_users_route import get_all_users_router
from src.modules.user.application.web.schemas.user_response_schema import UserResponseSchema
from src.modules.user.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_GetAllUsersRoute:

    def test_get_all_users(self):

        client = TestClient(app=app)

        all_users = client.get('/user/get_all_users')

        response = UserRepositoryMock().users

        
        response = [UserResponseSchema.model_validate(user).model_dump(mode='json') for user in response]


        assert all_users.status_code == 200
        assert all_users.json() == response

