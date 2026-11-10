
from src.shared.errors.base_error import BaseError


class DatabaseError(BaseError):

    def __init__(self) -> None:
        super().__init__("We couldn't connect to the database. Please try again later. We apologize for the inconvenience.")