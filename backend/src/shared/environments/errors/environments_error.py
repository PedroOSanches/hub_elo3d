from src.shared.errors.base_error import BaseError


class EnvironmentError(BaseError):
    def __init__(self, variable: str) -> None:
        super().__init__(f'Missing {variable} in environments')