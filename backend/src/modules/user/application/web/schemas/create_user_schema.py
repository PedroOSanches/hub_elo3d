import uuid
import re
from typing import Any

from pydantic import BaseModel, Field, EmailStr, ValidationError, model_validator, ConfigDict, field_validator
from pydantic_extra_types.phone_numbers import PhoneNumber
from src.shared.errors.controller_error import MissingParameters, WrongTypeParameter
from src.modules.user.domain.entities.endereco import Address
from src.modules.user.domain.enums.role_enum import ROLE

class CreateUserRequestSchema(BaseModel):
    
    name: str = Field(
        ...
    )

    email: str = Field(
        ...,
        description="E-mail do usuário"
    )

    password: str = Field(
        ...,
        min_length=8,
        description="Senha do usuário"
    )

    phone: str = Field(
        ...
    )

    address: CreateUserAddressSchema = Field(
        ...
    )

    institution_id: uuid.UUID | None = None

    role: ROLE = Field(
        ...,
        examples=['hospital', 'user_hospital', 'admin', ]
    )

    @field_validator("password")
    @classmethod
    def validate_password(cls, password: str) -> str:
        if not re.search(r"[a-z]", password):
            raise ValueError("Password must contain a lowercase letter")

        if not re.search(r"[A-Z]", password):
            raise ValueError("Password must contain an uppercase letter")

        if not re.search(r"\d", password):
            raise ValueError("Password must contain a number")

        if not re.search(r"[@$!%*?&]", password):
            raise ValueError("Password must contain a special character")

        return password

    role: ROLE = Field(
        ...,
        examples=['hospital', 'user_hospital', 'admin', 'user' ]
    )

    @model_validator(mode='wrap')
    @classmethod
    def validar_modelo(cls, value: Any, handler: Any) -> "CreateUserRequestSchema":
        if not value.get("name"): 
            raise MissingParameters('name')
        if not value.get('email'):
            raise MissingParameters('email')
        if not value.get('role'):
            raise MissingParameters('role')
        if not value.get('address'):
            raise MissingParameters('address')
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
                field_type_expected=str(
                    cls.model_fields[str(err.errors()[0]["loc"][0])].annotation
                ),
            ) from err


class CreateUserResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    user_id: uuid.UUID
    name: str
    email: EmailStr
    phone: PhoneNumber
    address: Address
    institution_id: uuid.UUID | None = None


class CreateUserAddressSchema(BaseModel):
    logradouro: str = Field(...)
    numero: str = Field(...)
    bairro: str = Field(...)
    cidade: str = Field(...)
    estado: str = Field(...)
    cep: str = Field(...)
    complemento: str | None = Field(default=None)

    model_config = ConfigDict(populate_by_name=True)

    @model_validator(mode="wrap")
    @classmethod
    def validar_schema(cls, value: Any, handler: Any) -> "CreateUserAddressSchema":
        if not isinstance(value, dict):
            raise WrongTypeParameter(
                field_name="address",
                field_type_received=type(value).__name__,
                field_type_expected="dict",
            )

        for field in ("logradouro", "numero", "bairro", "cidade", "estado"):
            if not value.get(field):
                raise MissingParameters(f"address.{field}")
        if "cep" not in value or value["cep"] is None:
            raise MissingParameters("address.cep")

        try:
            return handler(value)
        except ValidationError as err:
            field_name = str(err.errors()[0]["loc"][0])
            raise WrongTypeParameter(
                field_name=field_name,
                field_type_received=type(err.errors()[0]["input"]).__name__,
                field_type_expected=str(cls.model_fields[field_name].annotation),
            ) from err