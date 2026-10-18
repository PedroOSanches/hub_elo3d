import pytest

from uuid import UUID
from src.modules.user.infra.repositories.user_repository_mock import UserRepositoryMock, User, Address, NoUsersFound, DuplicatedUser


class Test_UserRepositoryMock:

    def test_create_user(self):
        repo = UserRepositoryMock()
        users = repo.users
        user = User(
            id="0334c795-5e71-4c1e-8a0e-ab21a4fcdecf",
            name = "Pedro",
            email="pedro@aacd.com",
            address=Address(
                logradouro="teste",
                numero="564",
                bairro="Novo Teste",
                cidade="Bragança Teste",
                cep="00000-000",
                estado="SP",
                complemento="Apto. 13"
            ),
            phone="+5511999999999",
            role="admin"
        )

        repo.create_user(user=user)

        assert users[-1] == user
        assert users[-1].id == UUID('0334c795-5e71-4c1e-8a0e-ab21a4fcdecf')

    def test_get_user(self):
        repo = UserRepositoryMock()

        users = repo.users

        user = repo.get_user("b189d11a-25d1-430e-b5a1-c53db528337e")

        assert users[0] == user
    
    def test_get_all_user(self):
        repo = UserRepositoryMock()

        users = repo.users

        get_all_user = repo.get_all_users()

        assert users == get_all_user

    def test_delete_user(self):
        repo = UserRepositoryMock()

        user = repo.get_all_users()[0]

        deleted_user = repo.delete_user("b189d11a-25d1-430e-b5a1-c53db528337e")

        assert user == deleted_user

    def test_update_user(self):
        repo = UserRepositoryMock()
        user = User(
            id="b189d11a-25d1-430e-b5a1-c53db528337e",
            name = "Miguel",
            email="miguel@aacd.com",
            address=Address(
                    logradouro="Rua Teste",
                    bairro="Teste",
                    cidade="Joateste",
                    cep="00000-000",
                    numero="S/N",
                    complemento="Casa",
                    estado="SP"
                ),
            phone="+5511999999999",
            role="admin"
        )

        repo_users = repo.users

        user = repo.update_user(updated_user=user)

        assert user == repo_users[0]

    def test_notfound_get_user(self):
        repo = UserRepositoryMock()

        with pytest.raises(NoUsersFound):
            repo.get_user("0334c795-5e71-4c1e-8a0e-ab21a4fcdecf")

    def test_notfound_update_user(self):
            repo = UserRepositoryMock()
    
            with pytest.raises(NoUsersFound):
                repo.update_user(
                    User(
                        id="0334c795-5e71-4c1e-8a0e-ab21a4fcdecf",
                        name = "Miguel",
                        email="miguel@aacd.com",
                        address=Address(
                            logradouro="Rua Teste",
                            bairro="Teste",
                            cidade="Joateste",
                            cep="00000-000",
                            numero="S/N",
                            complemento="Casa",
                            estado="SP"
                            ),
                        phone="+5511999999999",
                        role="admin"
        )
                )

    def test_notfound_delete_user(self):
        repo = UserRepositoryMock()
    
        with pytest.raises(NoUsersFound):
            repo.delete_user('0334c795-5e71-4c1e-8a0e-ab21a4fcdecf')

    def test_duplicated_user(self):
        repo = UserRepositoryMock()

        with pytest.raises(DuplicatedUser):
            repo.create_user(
                User(
                    name = "User",
                    email="user@example.com",
                    address=Address(
                        logradouro="Rua Teste",
                        bairro="Teste",
                        cidade="Joateste",
                        cep="00000-000",
                        numero="S/N",
                        complemento="Casa",
                        estado="SP"
                        ),
                    phone="+5511999999999",
                    role="admin"
                )
            )