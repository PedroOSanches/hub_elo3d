from .base_error import BaseError

class MissingParameters(BaseError):
    def __init__(self, field: str) -> None:
        super().__init__(f"Field '{field}' is missing")

class WrongTypeParameter(BaseError):
    def __init__(self, field_name: str, field_type_received: str, field_type_expected: str) -> None:
        super().__init__(
            f"The field '{field_name}' has the wrong type. Received: {field_type_received}. "
            f"Expected: {field_type_expected}"
        )