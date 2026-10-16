import hashlib

from uuid import UUID

from src.modules.user.domain.entities.user import User
from src.modules.user.domain.repositories.user_repository_interface import IUserRepository
from src.shared.utils.password_hasher import gerar_hash_senha

class CreateUserUsecase:

    def __init__(self, repo: IUserRepository):
        self.repo = repo

    def __call__(
            self, 
            name: str, 
            email: str, 
            phone: str, 
            institution_id: UUID, 
            password: str):

         user = User(
            name=name,
            email=email,
            phone=phone,
            institution_id=institution_id,
            password_hash = gerar_hash_senha(password)
            )
         
         return self.repo.create_user(user=user)

        