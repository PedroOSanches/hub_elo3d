import pytest
from src.modules.user.domain.entities.user import User, EntitieError, Address
from uuid import UUID

class TestUser:

    def test_user(self):
        user = User(
            name="User",
            email="user@example.com",
            phone="+5511999999999",
            role="user",
            password_hash="5156BECBC019E3F0F9520B143435427E",
            address=Address(
                    street="Rua Teste",
                    neighborhood="Teste",
                    cep="00000-000",
                    number="S/N",
                    address_details="Casa",
                    city="Teste",
                    state="SP"
                )
            
        )

    def test_institucional_user(self):
        user = User(
            name="User",
            email="user@institution.com",
            phone="+5599999999999",
            role="user",
            password_hash="5156BECBC019E3F0F9520B143435427E",
            address=Address(
                    street="Rua Teste",
                    neighborhood="Teste",
                    cep="00000-000",
                    number="S/N",
                    address_details="Casa",
                    city="Teste",
                    state="SP"
                )
        )

    def test_email_invalid(self):
        with pytest.raises(EntitieError):
            user = User(
                name="User",
                email="userinstitution.com",
                phone="+5599999999999",
                role="user",
                password_hash="5156BECBC019E3F0F9520B143435427E",
                address=Address(
                    street="Rua Teste",
                    neighborhood="Teste",
                    cep="00000-000",
                    number="S/N",
                    address_details="Casa",
                    city="Teste",
                    state="SP"
                )
            )
    def test_phone_invalid(self):
        with pytest.raises(EntitieError):
            user = User(
                name="User",
                email="user@institution.com",
                phone="11999999999",
                role="user",
                password_hash="5156BECBC019E3F0F9520B143435427E",
                address=Address(
                    street="Rua Teste",
                    neighborhood="Teste",
                    cep="00000-000",
                    number="S/N",
                    address_details="Casa",
                    city="Teste",
                    state="SP"
                )
            )

    def test_name_invalid(self):
        with pytest.raises(EntitieError):
            user = User(
                name="u",
                email="user@institution.com",
                phone="+5511999999999",
                role="user",
                password_hash="5156BECBC019E3F0F9520B143435427E",
                address=Address(
                    street="Rua Teste",
                    neighborhood="Teste",
                    cep="00000-000",
                    number="S/N",
                    address_details="Casa",
                    city="Teste",
                    state="SP"
                )
            )
    def test_password_hash_invalid(self):
        with pytest.raises(EntitieError):
            user = User(
                name="User",
                email="user@institution.com",
                phone="+5511999999999",
                role="admin",
                password_hash="5",
                address=Address(
                    street="Rua Teste",
                    neighborhood="Teste",
                    cep="00000-000",
                    number="S/N",
                    address_details="Casa",
                    city="Teste",
                    state="SP"
                )
            )

    def test_id_invalid(self):
            with pytest.raises(EntitieError):
                user = User(
                    user_id="u",
                    name="User",
                    email="user@institution.com",

                    phone="+5511999999999",
                    password_hash="5156BECBC019E3F0F9520B143435427E",
                    role="admin",
                    address=Address(
                    street="Rua Teste",
                    neighborhood="Teste",
                    cep="00000-000",
                    number="S/N",
                    address_details="Casa",
                    city="Teste",
                    state="SP"
                )
                )

    def test_role_invalid(self):
            with pytest.raises(EntitieError):
                user = User(
                    user_id="u",
                    name="User",
                    email="user@institution.com",

                    phone="+5511999999999",
                    password_hash="5156BECBC019E3F0F9520B143435427E",
                    role="a",
                    address=Address(
                    street="Rua Teste",
                    neighborhood="Teste",
                    cep="00000-000",
                    number="S/N",
                    address_details="Casa",
                    city="Teste",
                    state="SP"
                )
                )
        