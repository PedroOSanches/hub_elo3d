import pytest
from src.modules.user.domain.entities.user import User

class TestUser:

    def test_user(self):
        user = User(
            name="User",
            email="user@example.com",
            phone="+5511999999999",
            _password_hash="5156BECBC019E3F0F9520B143435427E"
        )