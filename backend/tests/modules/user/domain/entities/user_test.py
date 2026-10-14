import pytest
from src.modules.user.domain.entities.user import User, EntitieError

class TestUser:

    def test_user(self):
        user = User(
            name="User",
            email="user@example.com",
            phone="+5511999999999",
            password_hash="5156BECBC019E3F0F9520B143435427E"
            
        )

    def test_institucional_user(self):
        user = User(
            name="User",
            email="user@institution.com",
            institution_id="bd6987dc-8298-4c03-9ccd-91f2ebdbe28a",
            phone="+5599999999999",
            password_hash="5156BECBC019E3F0F9520B143435427E"
        )

    def test_email_invalid(self):
        with pytest.raises(EntitieError):
            user = User(
                name="User",
                email="userinstitution.com",
                institution_id="bd6987dc-8298-4c03-9ccd-91f2ebdbe28a",
                phone="+5599999999999",
                password_hash="5156BECBC019E3F0F9520B143435427E"
            )
    def test_phone_invalid(self):
        with pytest.raises(EntitieError):
            user = User(
                name="User",
                email="user@institution.com",
                institution_id="bd6987dc-8298-4c03-9ccd-91f2ebdbe28a",
                phone="11999999999",
                password_hash="5156BECBC019E3F0F9520B143435427E"
            )

    def test_name_invalid(self):
        with pytest.raises(EntitieError):
            user = User(
                name="u",
                email="user@institution.com",
                institution_id="bd6987dc-8298-4c03-9ccd-91f2ebdbe28a",
                phone="+5511999999999",
                password_hash="5156BECBC019E3F0F9520B143435427E"
            )
    def test_password_hash_invalid(self):
        with pytest.raises(EntitieError):
            user = User(
                name="User",
                email="user@institution.com",
                institution_id="bd6987dc-8298-4c03-9ccd-91f2ebdbe28a",
                phone="+5511999999999",
                password_hash="5"
            )
    def test_institution_id_invalid(self):
        with pytest.raises(EntitieError):
            user = User(
                name="User",
                email="user@institution.com",
                institution="b",
                phone="+5511999999999",
                password_hash="5156BECBC019E3F0F9520B143435427E"
            )

    def test_id_invalid(self):
            with pytest.raises(EntitieError):
                user = User(
                    id="u",
                    name="User",
                    email="user@institution.com",
                    institution="b",
                    phone="+5511999999999",
                    password_hash="5156BECBC019E3F0F9520B143435427E"
                )
        