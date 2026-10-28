from pydantic import BaseModel, EmailStr, model_validator, ValidationError
from src.shared.errors.controller_error import WrongTypeParameter
from typing import Any



class LoginRequestSchema(BaseModel):
    email: EmailStr
    password: str


    @model_validator(mode='wrap')
    @classmethod
    def valida_chamada(cls, value: Any, handler: Any) -> "LoginRequestSchema":
        try:
            return handler(value)
        except ValidationError as err:
            raise WrongTypeParameter(
                field_name=str(err.errors()[0]["loc"][0]),
                field_type_received=type(err.errors()[0]["input"]).__name__,
                field_type_expected=str(cls.model_fields[str(err.errors()[0]["loc"][0])].annotation)
            ) from err