from base_error import BaseError

class EntitieError(BaseError):

    def __init__(self, field: str) -> None:
        super().__init__(f"Field {field} is not valid")