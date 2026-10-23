from typing import Any, ClassVar

from pydantic import BaseModel, ConfigDict, ValidationError, model_validator

from src.shared.errors.controller_error import MissingParameters, WrongTypeParameter


class BaseRequestSchema(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    campos_obrigatorios: ClassVar[tuple[str, ...]] = ()

    @model_validator(mode="wrap")
    @classmethod
    def validar_modelo(cls, value: Any, handler: Any) -> "BaseRequestSchema":
        if isinstance(value, dict):
            for campo in cls.campos_obrigatorios:
                valor = value.get(campo)
                if valor is None or (isinstance(valor, str) and not valor.strip()):
                    raise MissingParameters(campo)
        try:
            return handler(value)
        except ValidationError as err:
            erro = err.errors()[0]
            campo = str(erro["loc"][0]) if erro["loc"] else "body"
            campo_info = cls.model_fields.get(campo)
            raise WrongTypeParameter(
                field_name=campo,
                field_type_received=type(erro["input"]).__name__,
                field_type_expected=campo_info.annotation if campo_info else "unknown",
            ) from err