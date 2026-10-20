from typing import Any
from pydantic import BaseModel, Field, ValidationError, model_validator, ConfigDict
from src.shared.errors.controller_error import MissingParameters, WrongTypeParameter
from uuid import UUID

from src.modules.user.domain.entities.endereco import Address
from src.modules.user.domain.enums.role_enum import ROLE


class GetUserRequestSchema(BaseModel):

    id: UUID = Field(
        ...
    )

    @model_validator(mode='wrap')
    @classmethod
    def validar_schema(cls, value: Any, handler: Any) -> "GetUserRequestSchema":
        if not value.get('id'):
            raise MissingParameters('id')

        try:
            return handler(value)
        except ValidationError as err:
            raise WrongTypeParameter(
                field_name=str(err.errors()[0]["loc"][0]),
                field_type_received=type(err.errors()[0]["input"]).__name__,
                field_type_expected=str(cls.model_fields[str(err.errors()[0]["loc"][0])].annotation.__name__)
            ) from err