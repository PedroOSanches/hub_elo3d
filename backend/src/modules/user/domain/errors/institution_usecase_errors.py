from src.shared.errors.usecase_error import BaseError

class NoInstitutionFound(BaseError):
    def __init__(self, id: str):
        super().__init__(f'No institution found with id: {id}')

class DuplicatedInstitution(BaseError):
    def __init__(self):
        super().__init__(f'The institution already exists.')
