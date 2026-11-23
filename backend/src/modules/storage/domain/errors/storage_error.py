from src.shared.errors.base_error import BaseError


class StorageError(BaseError):
    def __init__(self) -> None:
        super().__init__('An error occurred while processing the file in storage.')
