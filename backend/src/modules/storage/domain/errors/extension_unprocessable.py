from src.shared.errors.usecase_error import UnprocessableEntity


class ExtensionUnprocessableError(UnprocessableEntity):
    def __init__(self, extension: str) -> None:
        super().__init__(f"The file extension '{extension}' is not supported.")