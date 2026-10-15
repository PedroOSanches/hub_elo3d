from .base_error import BaseError

class NotFoundError(BaseError):
    pass

class DuplicatedError(BaseError):
    pass

class ForbiddenAction(BaseError):
    def __init__(self, message: str):
        super().__init__(f'That action is forbidden for this {message}')
