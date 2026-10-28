from src.modules.auth.domain.gateways.gateway_user_interface import IGatewayUser
from src.modules.auth.domain.entities.auth_user import AuthUser
from src.modules.user.domain.errors.user_usecase_errors import NoUsersFound
from src.modules.user.domain.repositories.user_repository_interface import IUserRepository
from src.modules.user.application.web.dependencies import get_repo_user

class GatewayUser(IGatewayUser):

    def __init__(self, repo: IUserRepository) -> None:
        self.repo = repo
    def get_user_by_email(self, email: str) -> AuthUser:
            user = self.repo.get_user_by_email(email)
            return AuthUser(
                id=user.id,
                email=user.email,
                password_hash=user.password_hash if user.password_hash is not None else "Error",
                role=user.role
            )

    @classmethod
    def get_repo_user(cls):
        return get_repo_user()