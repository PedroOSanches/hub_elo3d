from src.shared.errors.domain_error import UnauthorizedAction

class InvalidCredentials(UnauthorizedAction):

    def __init__(self) -> None:
        super().__init__(msg="Invalid email or password")


class AuthUnathorizedAction(UnauthorizedAction):

    def __init__(self) -> None:
        super().__init__(msg='Authentication Failed')