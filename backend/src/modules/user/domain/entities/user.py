import uuid
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from pydantic_extra_types.phone_numbers import PhoneNumber

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


    instituicao: uuid.UUID | None = Field(
        ...,
        description="Identificador da instituição que o usuário pertence."
    )
    telefone: PhoneNumber | None = Field(
        ...,
        description="Número de telefone do usuário"
    )
    _password_hash: str = Field(
        ...,
        description="Hash da senha do usuário",
        min_length=2,
        repr=False,
    )

    model_config = ConfigDict(
        use_enum_values=True,
        extra='forbid',
        populate_by_name=True
    )