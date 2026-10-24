from typing import Any
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
            id: UUID,
            *,
            new_name: str | None,
            new_phone: PhoneNumber | None,
            new_address: UpdateAddressRequestSchema | None,
            new_password: str | None
            ) -> Any:

        stored_user = self.repo.get_user(id=id)

        user = User(
            id=id,
            name=new_name or stored_user.name,
            email=stored_user.email,
            address= Address(
                logradouro = new_address.new_logradouro or stored_user.address.logradouro,
                numero = new_address.new_numero or stored_user.address.numero,
                bairro = new_address.new_bairro or stored_user.address.bairro,
                cidade = new_address.new_cidade or stored_user.address.cidade,
                cep = new_address.new_cep or stored_user.address.cep,
                estado = new_address.new_estado or stored_user.address.estado,
            ) if new_address is not None else stored_user.address,
            role=stored_user.role,
            phone=new_phone or stored_user.phone,
            password_hash=gerar_hash_senha(new_password) if new_password is not None else stored_user.password_hash
        )

        return self.repo.update_user(updated_user=user)
