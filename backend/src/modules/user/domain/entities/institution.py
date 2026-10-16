import pydantic
import uuid

from typing import Any
from pydantic import (
    BaseModel, 
    Field, 
    model_validator, 
    ModelWrapValidatorHandler, 
    ValidationError,
    ConfigDict
)

from src.shared.errors.domain_error import EntitieError

class Institution(BaseModel):

    id: uuid.UUID = Field(
        default=uuid.uuid4(),
        description="Identificador único da instituição"
    )

    name: str = Field(
        ...,
        description="Nome da Instituição",
        examples=["Instituto Mauá de Tecnologia", "AACD"]
    )

    description: str | None = Field(
        default=None,
        description="Descrição da instituição",
        examples=["O IMT é parceiro da AACD, disponibilizando seu FabLab para fabricação de Proteses e Órteses produzidas a partir de impressão 3D"]
    )

    model_config = ConfigDict(
        use_enum_values=True,
        extra='forbid',
        populate_by_name=True
    )

    @model_validator(mode='wrap')
    @classmethod
    def validar_modelo(cls, data: Any, handler: ModelWrapValidatorHandler) -> "Institution":
        try:
            return handler(data)
        except ValidationError as err:
            raise EntitieError(str(err.errors()[0]["loc"][0])) from err
        