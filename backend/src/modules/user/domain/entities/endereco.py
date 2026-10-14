import uuid
from pydantic import BaseModel, Field

class Endereco(BaseModel):

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