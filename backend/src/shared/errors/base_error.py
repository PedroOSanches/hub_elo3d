class BaseError(Exception):
    def __init__(self, msg: str) -> None:
        self.message = msg
        super().__init__(self._msg)

    @property
    def message(self):
        return self._msg

    @message.setter
    def message(self, value: str):
        self._msg = value