from pydantic import BaseModel, ConfigDict, Field


class UploadFileRequest(BaseModel):

    file_name: str = Field(
        ...,
        min_length=3
    )

    size: int = Field(
        ...,
        gt=0
    )

    content_type: str = Field(
        ...,
        )

    model_config = ConfigDict(
        extra='forbid'
    )

class GenerateUrlRequestSchema(BaseModel):
    
    files: list[UploadFileRequest] = Field(
        ..., 
        min_length=1
        )

    model_config = ConfigDict(
        extra='forbid'
    )