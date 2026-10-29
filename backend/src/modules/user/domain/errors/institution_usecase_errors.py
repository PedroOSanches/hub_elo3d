from src.shared.errors.usecase_error import BaseError

class NoInstitutionFound(BaseError):
    def __init__(self, user_id: str):
        super().__init__(f'No institution found with user_id: {user_id}')

class DuplicatedInstitution(BaseError):
    def __init__(self):
        super().__init__(f'The institution already exists.')
