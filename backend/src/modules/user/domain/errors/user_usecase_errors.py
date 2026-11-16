from src.shared.errors.usecase_error import DuplicatedError, NotFoundError


class NoUsersFound(NotFoundError):
    def __init__(self, message: str):
        super().__init__(f'No users found for {message}')

class DuplicatedUser(DuplicatedError):
    def __init__(self, message: str):
        super().__init__(f'The user already exists for this {message}')
