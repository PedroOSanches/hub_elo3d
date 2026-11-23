from src.shared.errors.usecase_error import NotFoundError


class FileNotFound(NotFoundError):
    def __init__(self, file_name: str) -> None:
        super().__init__(f"The file '{file_name}' could not be found.")