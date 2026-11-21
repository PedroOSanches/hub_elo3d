from pydantic import RootModel

from src.modules.project.application.web.schemas.create_project_schema import (
    CreateProjectResponseSchema,
)


class GetAllProjectsResponseSchema(RootModel[list[CreateProjectResponseSchema]]):
    pass