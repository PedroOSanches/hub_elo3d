from pydantic import BaseModel, Field, ConfigDict

class ProjectFile(BaseModel):
    title: str = Field(
        ...,
        min_length = 1,
        description = "Título do arquivo do projeto"
    )

    file_url: str = Field(
        ...,
        min_length = 1,
        description = "URL do arquivo do projeto"
    )

    model_config = ConfigDict(
        extra = "forbid"
    )