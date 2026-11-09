from uuid import UUID

from pydantic_extra_types.phone_numbers import PhoneNumber
from src.modules.user.domain.entities.user import User, Address
from src.modules.user.domain.repositories.user_repository_interface import IUserRepository
from src.modules.user.application.web.schemas.update_user_request_schema import UpdateAddressRequestSchema

from src.shared.utils.password_hasher import gerar_hash_senha

class UpdateUserUsecase:

    def __init__(self, repo: IUserRepository) -> None:
        self.repo = repo

    def __call__(
            self,
            user_id: UUID,
            *,
            new_name: str | None,
            new_phone: PhoneNumber | None,
            new_address: UpdateAddressRequestSchema | None,
            new_password: str | None
            ) -> User:

        stored_user = self.repo.get_user(user_id=user_id)

        user = User(
            user_id=user_id,
            name=new_name or stored_user.name,
            email=stored_user.email,
            address= Address(
                street = new_address.new_street or stored_user.address.street,
                number = new_address.new_number or stored_user.address.number,
                neighborhood = new_address.new_neighborhood or stored_user.address.neighborhood,
                city = new_address.new_city or stored_user.address.city,
                cep = new_address.new_cep or stored_user.address.cep,
                state = new_address.new_state or stored_user.address.state,
                address_details=new_address.new_address_details or stored_user.address.address_details
            ) if new_address is not None else stored_user.address,
            role=stored_user.role,
            phone=new_phone or stored_user.phone,
            institution_id=stored_user.institution_id,
            password_hash=gerar_hash_senha(new_password) if new_password is not None else stored_user.password_hash
        )

        return self.repo.update_user(updated_user=user)
