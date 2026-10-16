import uuid
from typing import Any

from pydantic import BaseModel, Field, EmailStr, ValidationError, ModelWrapValidatorHandler, model_validator
from pydantic_extra_types.phone_numbers import PhoneNumber
from src.shared.errors.controller_error import MissingParameters, WrongTypeParameter
from src.modules.user.domain.entities.endereco import Address

class CreateUserRequestSchema(BaseModel):
    
    name: str = Field(
        ...
    )

    email: EmailStr = Field(
        ...,
        description="E-mail do usuário"
    )

    password: str = Field(
        ...,
        description="Senha do usuário"
    )

    phone: PhoneNumber = Field(
        ...
    )

    address: Address = Field(
        ...
    )

    institution_id: uuid.UUID | None

    @model_validator(mode='wrap')
    @classmethod
    def validadar_modelo(cls, value: Any, handler: Any) -> "CreateUserRequestSchema":
        if not value.get("name"): 
            raise MissingParameters('name')
        if not value.get('email'):
            raise MissingParameters('email')
        if not value.get('phone'):
            raise MissingParameters('phone')
        if not value.get('password'):
            raise MissingParameters('password')
        try:
            return handler(value)
        except ValidationError as err:
            raise WrongTypeParameter(
                field_name=str(err.errors()[0]["loc"][0]),
                field_type_received=type(err.errors()[0]["input"]).__name__,
                field_type_expected=str(cls.model_fields[str(err.errors()[0]["loc"][0])].annotation)
            ) from err


class CreateUserResponseSchema(BaseModel):
    id: uuid.UUID
    name: str
    email: EmailStr
    phone: PhoneNumber
    address: Address
    institution: uuid.UUID | None

