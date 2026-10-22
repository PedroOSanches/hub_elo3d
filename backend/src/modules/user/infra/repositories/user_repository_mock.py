from src.modules.user.domain.repositories.user_repository_interface import IUserRepository 
from  src.modules.user.domain.entities.user import User
from  src.modules.user.domain.entities.endereco import Address
from  src.modules.user.domain.errors.user_usecase_errors import NoUsersFound, DuplicatedUser
from uuid import UUID

class UserRepositoryMock(IUserRepository):
    def __init__(self):
        self.users = [
            User(
                id = "b189d11a-25d1-430e-b5a1-c53db528337e",
                name="User",
                email="user@example.com",
                phone="+5511999999999",
                address=Address(
                    logradouro="Rua Teste",
                    bairro="Teste",
                    cep="00000-000",
                    cidade="São Teste do Sul",
                    numero="S/N",
                    complemento="Casa",
                    estado="SP"
                ),
                role="user"
                ),
                User(
                    id = "b189d11a-25d1-430e-b5a1-c53db528337e",
                    name="User AACD",
                    email="user@aacd.com",
                    phone="+5511999999999",
                    address=Address(
                        logradouro="Rua Teste",
                        bairro="Teste",
                        cep="00000-000",
                        cidade="São Teste do Sul",
                        numero="S/N",
                        complemento="Casa",
                        estado="SP"
                    ),
                    role="hospital"
                    ),
                    User(
                        id = "b189d11a-25d1-430e-b5a1-c53db528337e",
                        name="User Maua",
                        email="user@maua.br",
                        phone="+5511999999999",
                        address=Address(
                            logradouro="Rua Teste",
                            bairro="Teste",
                            cep="00000-000",
                            cidade="São Teste do Sul",
                            numero="S/N",
                            complemento="Casa",
                            estado="SP"
                        ),
                        role="admin"
                        ),
        ]

    def get_user(self, id: UUID) -> User:
        if isinstance(id, str):
            id = UUID(id)

        for user in self.users:
            if user.id == id:
                return user
            
        raise NoUsersFound(f"id: '{str(id)}'")

    def get_all_users(self) -> list[User]:
        return self.users

    def create_user(self, user: User) -> User:
        for stored_user in self.users:
            if user.email == stored_user.email:
                raise DuplicatedUser(f'email: {user.email}')
        
        self.users.append(user)

        return user
    
    def update_user(self,  updated_user: User) -> User:
        for i, user in enumerate(self.users):
            if updated_user.id == user.id:
                self.users[i] = updated_user
                return self.users[i]

        raise NoUsersFound(f'id: {id}')

    def delete_user(self, id: str) -> User:
        for i, user in enumerate(self.users):
            if id == str(user.id):
                return self.users.pop(i)

        raise NoUsersFound(f"id: {id}")

    
