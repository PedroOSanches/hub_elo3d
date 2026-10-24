from uuid import UUID
from pydantic import BaseModel, Field, ValidationError, model_validator, ConfigDict
from pydantic_extra_types.phone_numbers import PhoneNumber
from src.shared.errors.controller_error import MissingParameters, WrongTypeParameter


from typing import Any

class UpdateUserRequestSchema(BaseModel):
    id: UUID = Field(
        ...
    )
    new_name: str | None = Field(
        default=None
    )
    new_password: str | None = Field(
        default=None
    )
    address: UpdateAddressRequestSchema | None = Field(
        default=None
    )
    new_phone: PhoneNumber | None = Field(
        default=None
    )

    @model_validator(mode='wrap')
    @classmethod
    def validar_request(cls, value: Any, handler: Any) -> "UpdateUserRequestSchema":
        try:
            return handler(value)
        except ValidationError as err:
            raise WrongTypeParameter(
                field_name=str(err.errors()[0]["loc"][0]),
                field_type_received=type(err.errors()[0]["input"]).__name__,
                field_type_expected=str(cls.model_fields[str(err.errors()[0]["loc"][0])].annotation)
            ) from err

class UpdateAddressRequestSchema(BaseModel):
    new_logradouro: str | None = Field(
        default=None,
        )
    new_numero: str | None = Field(
        default=None,
        )
    new_bairro: str | None = Field(
        default=None,
    )
    new_cidade: str | None = Field(
        default=None,
    )
    new_estado: str | None = Field(
        default=None,
    )
    new_cep: str | None = Field(
        default=None,
    )
    new_complemento: str | None = Field(
        default=None,
    )