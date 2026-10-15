from src.shared.errors.usecase_error import BaseError

class NoUsersFound(BaseError):
    def __init__(self, message: str):
        super().__init__(f'No users found for {message}')

class DuplicatedUser(BaseError):
    def __init__(self, message: str):
        super().__init__(f'The user already exists for this {message}')
