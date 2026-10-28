import uuid
from typing import Any
from pydantic import (
    BaseModel, 
    EmailStr, 
    Field, 
    ConfigDict, 
    ValidationError, 
    model_validator, 
    ModelWrapValidatorHandler
    )

from pydantic_extra_types.phone_numbers import PhoneNumber

from .endereco import Address
from src.shared.errors.domain_error import EntitieError
from src.modules.user.domain.enums.role_enum import ROLE

class User(BaseModel):
    user_id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        description="Identificador único de usuário"
    ) 
    name: str = Field(
        ...,
        min_length=3,
        description="Nome do Usuário"
    )

    email: EmailStr = Field(
        ...,
        description="Email do usuário",
        examples=["user@example.com", "user@aacd.com"]
    )

    institution_id: uuid.UUID | None = Field(
        default=None,
        description="Identificador da instituição que o usuário pertence."
    )

    address: Address = Field(
        ...,
        description="Endereço do usuário"
    )

    phone: PhoneNumber | None = Field(
        ...,
        description="Número de telefone do usuário"
    )
    password_hash: str | None = Field(
        default=None,
        description="Hash da senha do usuário",
        min_length=2,
        exclude=True,
    )

    role: ROLE = Field(
        ...,
        description="As funções que o usuário tem no sistema"
    )


    model_config = ConfigDict(
        use_enum_values=True,
        extra='forbid',
        populate_by_name=True
    )

    @model_validator(mode='wrap')
    @classmethod
    def validar_modelo(cls, data: Any, handler: ModelWrapValidatorHandler) -> "User":
        try:
            return handler(data)
        except ValidationError as err:
            raise EntitieError(str(err.errors()[0]["loc"][0])) from err
    