import uuid
from pydantic import BaseModel, EmailStr, Field, ConfigDict, ValidationError
from pydantic_extra_types.phone_numbers import PhoneNumber

from .endereco import Endereco
from src.shared.errors.domain_error import EntitieError

class User(BaseModel):
    id: uuid.UUID = Field(
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

    phone: PhoneNumber | None = Field(
        ...,
        description="Número de telefone do usuário"
    )
    password_hash: str = Field(
        default=None,
        description="Hash da senha do usuário",
        min_length=2,
        repr=False,
    )

    model_config = ConfigDict(
        use_enum_values=True,
        extra='forbid',
        populate_by_name=True
    )

    def __init__(self, **data):
        try:
            super().__init__(**data)
        except ValidationError as err:
            raise EntitieError(str(err.errors()[0]["loc"][0])) from err
    