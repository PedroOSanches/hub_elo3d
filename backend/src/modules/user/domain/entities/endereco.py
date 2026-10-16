from typing import Any
import uuid
from src.shared.errors.domain_error import EntitieError
from pydantic import BaseModel, Field, ConfigDict, model_validator, ModelWrapValidatorHandler, ValidationError

class Address(BaseModel):

    logradouro: str = Field(
        ...,
        min_length=5,
        examples=["Praça Mauá", "Av. dos Estados"]
    )

    numero: str = Field(
        ...,
        min_length=1,
        examples=["S/N", "234"]
    )
    bairro: str = Field(
        ...,
        examples=["Sé", "Jardim Bela Vista"]
    )
    estado: str = Field(
        ...,
        min_length=2,
        max_length=2,
        examples=["SP", "MG", "PI"]
    )

    cep: str = Field(
        ...,
        min_length=9,
        max_length=9,
        examples=["12980-000", "09572-550"]
    )

    complemento: str = Field(
        ...,
        examples=["Apto. 51", "Casa"]
    )

    model_config = ConfigDict(
        use_enum_values=True,
        extra="forbid",
        populate_by_name=True
    )

    @model_validator(mode='wrap')
    @classmethod
    def validar_modelo(cls, data: Any, handler: ModelWrapValidatorHandler) -> "address":
        try:
            return handler(data)
        except ValidationError as err:
            raise EntitieError(str(err.errors()[0]["loc"][0])) from err
