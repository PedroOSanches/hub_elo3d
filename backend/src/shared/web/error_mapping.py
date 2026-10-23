from src.shared.errors.controller_error import WrongTypeParameter, MissingParameters
from src.shared.errors.domain_error import EntitieError
from src.shared.errors.usecase_error import NotFoundError, DuplicatedError, ForbiddenAction



ERROR_STATUS_CODES = {
    WrongTypeParameter: 422,
    MissingParameters: 422,
    NotFoundError: 404,
    EntitieError: 406,
    DuplicatedError: 409,
    ForbiddenAction: 401
}


def get_status_code(error: Exception) -> int:
    for error_class in type(error).__mro__:
        if error.__class__ in ERROR_STATUS_CODES:
            return ERROR_STATUS_CODES[error_class]

    return 500