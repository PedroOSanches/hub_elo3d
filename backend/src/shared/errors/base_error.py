class BaseError(Exception):
    def __init__(self, msg: str) -> None:
        self._msg = msg
        super().__init__(self._msg)