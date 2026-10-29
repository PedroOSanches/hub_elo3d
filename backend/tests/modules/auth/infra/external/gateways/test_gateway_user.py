import pytest

from src.modules.auth.infra.external.gateways.gateway_user import GatewayUser, NoUsersFound
from src.modules.user.infra.repositories.user_repository_mock import UserRepositoryMock
from uuid import UUID, uuid4

@pytest.fixture()
def gateway():
    repo = UserRepositoryMock()
    return GatewayUser(repo=repo)


class Test_GatewayUser:

    def test_gateway_user_get_user_by_email(self, gateway):

        user = gateway.get_user_by_email('user@example.com')

        assert user.role == 'user'

    def test_gateway_user_get_by_email_not_found(self, gateway):
        with pytest.raises(NoUsersFound):
            user = gateway.get_user_by_email('notfound@user.com')

    def test_gateway_user_get_by_id(self, gateway):
        user = gateway.get_user_by_id(UUID('20ba02d0-d00f-474b-ad43-10b76abba8ee'))

        assert user.role == 'hospital'
    
    def test_gateway_user_get_by_id_not_found(self, gateway):
        with pytest.raises(NoUsersFound):
            gateway.get_user_by_id(uuid4())