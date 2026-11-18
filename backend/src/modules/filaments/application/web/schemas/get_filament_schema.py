from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field, ValidationError, model_validator

from src.shared.errors.controller_error import MissingParameters, WrongTypeParameter


class GetFilamentRequestSchema(BaseModel):

    filament_id: UUID = Field(
        ...
    )

    @model_validator(mode='wrap')
    @classmethod
    def validar_schema(cls, value: Any, handler: Any) -> "GetFilamentRequestSchema":
        if not value.get('filament_id'):
            raise MissingParameters('filament_id')

        try:
            return handler(value)
        except ValidationError as err:
            raise WrongTypeParameter(
                field_name=str(err.errors()[0]["loc"][0]),
                field_type_received=type(err.errors()[0]["input"]).__name__,
                field_type_expected=str(cls.model_fields[str(err.errors()[0]["loc"][0])].annotation.__name__)
            ) from err