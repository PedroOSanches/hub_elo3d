from typing import Any

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    ModelWrapValidatorHandler,
    ValidationError,
    model_validator,
)

from src.modules.storage.domain.enums.contents_type_enum import ContentTypeEnum
from src.shared.errors.controller_error import MissingParameters, WrongTypeParameter


class UploadFileRequest(BaseModel):

    file_name: str = Field(
        ...,
        min_length=3
    )

    size: int = Field(
        ...,
        gt=0
    )

    content_type: ContentTypeEnum = Field(
        ...,
        )

    model_config = ConfigDict(
        extra='forbid'
    )

    @model_validator(mode='wrap')
    @classmethod
    def validar_modelo(
        cls, 
        data: Any, 
        handler: ModelWrapValidatorHandler
        ) -> UploadFileRequest:
        try:
            if not data.get('file_name'):
                raise MissingParameters('file_name')
            if not data.get('size'):
                raise MissingParameters('size')
            if not data.get('content_type'):
                raise MissingParameters('size')

            return handler(data)
        
        except ValidationError as err:
            field_name = str(err.errors()[0]["loc"][0])
            raise WrongTypeParameter(
                field_name=field_name, 
                field_type_received=type(err.errors()[0]["input"]).__name__, 
                field_type_expected=str(cls.model_fields[field_name].annotation),
                ) from err

class GenerateUrlRequestSchema(BaseModel):
    project_name: str = Field(
        ...
    )
    files: list[UploadFileRequest] = Field(
        ..., 
        min_length=1
        )

    model_config = ConfigDict(
        extra='forbid'
    )

    @model_validator(mode='wrap')
    @classmethod
    def validar_modelo(
        cls, 
        data: Any, 
        handler: ModelWrapValidatorHandler
        ) -> GenerateUrlRequestSchema:
        try:
            if not data.get('project_name'):
                raise MissingParameters('project_name')
            if not data.get('files'):
                raise MissingParameters('files')
    
            return handler(data)
    
        except ValidationError as err:
            field_name = str(err.errors()[0]["loc"][0])
            raise WrongTypeParameter(
                field_name=field_name, 
                field_type_received=type(err.errors()[0]["input"]).__name__, 
                field_type_expected=str(cls.model_fields[field_name].annotation),
                ) from err