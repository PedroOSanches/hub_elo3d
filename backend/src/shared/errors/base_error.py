class BaseError(Exception):
    def __init__(self, msg: str) -> None:
        self._msg = msg
        super().__init__(self._msg)


class EntitieError(BaseError):

    def __init__(self, field: str) -> None:
        super().__init__(f"Field {field} is not valid")