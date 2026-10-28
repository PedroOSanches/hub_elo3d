from ...domain.repositories.user_repository_interface import IUserRepository 
from ...domain.entities.user import User
from ...domain.errors.user_usecase_errors import NoUsersFound, DuplicatedUser


class UserRepositoryMock(IUserRepository):
    def __init__(self):
        self.users = [
            User(),
            User(),
            User()
        ]

    def get_user(self, id: str) -> User:
        for user in self.users:
            if str(user.id) == id:
                return user

        raise NoUsersFound(f"id: {id}")

    def get_all_users(self) -> list[User]:
        return self.users

    def create_user(self, user: User) -> User:
        for stored_user in self.users:
            if user.email == stored_user.email:
                raise DuplicatedUser(f'email: {user.email}')
        
        self.users.append(user)

        return user
    
    def update_user(self, id: str, updated_user: User) -> User:
        for i, user in enumerate(self.users):
            if id == str(user.id):
                self.users[i] = updated_user
                return self.users[i]

        raise NoUsersFound(f'id: {id}')

    def delete_user(self, id: str) -> User:
        for i, user in enumerate(self.users):
            if id == str(user.id):
                self.users.pop(i)

    
