
from pydantic import BaseModel, ConfigDict, Field, field_validator

from src.shared.errors.domain_error import EntitieError

ALLOWED_CONTENT_TYPES = {
    "model/stl",
    "model/obj",
    "model/3mf",
    "application/x-amf",
    "model/ply",
    "application/step",
    "text/x.gcode",
    "text/plain",
    "application/octet-stream",
    "application/pdf",
    "image/png",
    "image/jpeg",
    "application/zip",
}

class ProjectFile(BaseModel):
    title: str = Field(
        ...,
        min_length = 1,
        description = "Título do arquivo do projeto"
    )

    object_key: str = Field(
        description = "Chave do arquivo guardado na S3",
        min_length=5,
    )

    size: int = Field(
        gt=0
    )

    content_type: str = Field(
        description="Tipo MIME do arquivo",
        examples=['model/stl', "model/obj", "model/3mf"]
    )

    model_config = ConfigDict(
        extra = "forbid",
        use_enum_values=True
    )

    @field_validator("content_type", mode='before')
    @classmethod
    def content_type_validator(cls, value: str) -> str:
        value = value.strip().lower()
        if value not in ALLOWED_CONTENT_TYPES:
            raise EntitieError('content_type')

        return value