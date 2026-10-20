from uuid import UUID

from src.shared.errors.usecase_error import NotFoundError


class PrinterNotFoundError(NotFoundError):
    def __init__(self, printer_id: UUID) -> None:
        super().__init__(f"Printer {printer_id} not found")


class UserNotFoundError(NotFoundError):
    def __init__(self, user_id: UUID) -> None:
        super().__init__(f"User {user_id} not found")