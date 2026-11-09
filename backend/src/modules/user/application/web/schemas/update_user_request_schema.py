from uuid import UUID
from pydantic import BaseModel, Field, ValidationError, model_validator, ConfigDict
from pydantic_extra_types.phone_numbers import PhoneNumber
from src.shared.errors.controller_error import MissingParameters, WrongTypeParameter


from typing import Any

class UpdateUserRequestSchema(BaseModel):
    user_id: UUID = Field(
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
            if value.get('user_id') is None:
                raise MissingParameters('user_id')
            if (
                value.get('new_name') is None
                and value.get('new_password') is None
                and value.get('address') is None
                and value.get('new_phone') is None
            ):
                raise MissingParameters(['new_name', 'new_password', 'address', 'new_phone'])
            
            return handler(value)
        except ValidationError as err:
            raise WrongTypeParameter(
                field_name=str(err.errors()[0]["loc"][0]),
                field_type_received=type(err.errors()[0]["input"]).__name__,
                field_type_expected=str(cls.model_fields[str(err.errors()[0]["loc"][0])].annotation)
            ) from err

class UpdateAddressRequestSchema(BaseModel):
    new_street: str | None = Field(
        default=None,
        )
    new_number: str | None = Field(
        default=None,
        )
    new_neighborhood: str | None = Field(
        default=None,
    )
    new_city: str | None = Field(
        default=None,
    )
    new_state: str | None = Field(
        default=None,
    )
    new_cep: str | None = Field(
        default=None,
    )
    new_address_details: str | None = Field(
        default=None,
    )

    @model_validator(mode='wrap')
    @classmethod
    def validar_model(cls, value: Any, handler: Any) -> "UpdateAddressRequestSchema":
        try:
            if (
                value.get('new_street') is None
                and value.get('new_number') is None
                and value.get('new_neighborhood') is None
                and value.get('new_city') is None
                and value.get('new_state') is None
                and value.get('new_cep') is None
                and value.get('new_address_details') is None
            ):
                raise MissingParameters(['new_street', 'new_number', 'new_neighborhood', 'new_city', 'new_state', 'new_cep', 'new_address_details'])
            return handler(value)
        except ValidationError as err:
            raise WrongTypeParameter(
                field_name=str(err.errors()[0]["loc"][0]),
                field_type_received=type(err.errors()[0]["input"]).__name__,
                field_type_expected=str(cls.model_fields[str(err.errors()[0]["loc"][0])].annotation)
            ) from err