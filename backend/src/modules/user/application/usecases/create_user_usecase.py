import hashlib

from uuid import UUID

from pydantic_extra_types.phone_numbers import PhoneNumber 
from src.modules.user.domain.entities.user import User, Address
from src.modules.user.domain.repositories.user_repository_interface import IUserRepository
from src.shared.utils.password_hasher import gerar_hash_senha

class CreateUserUsecase:

    def __init__(self, repo: IUserRepository):
        self.repo = repo

    def __call__(
            self, 
            name: str, 
            email: str, 
            phone: PhoneNumber, 
            institution_id: UUID | None,
            address: Address,
            password: str) -> User:

        user = User(
            name=name,
            email=email,
            phone=phone,
            institution_id=institution_id,
            address=address,
            password_hash = gerar_hash_senha(password)
            )
        
        return self.repo.create_user(user=user)

        