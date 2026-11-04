from pydantic import RootModel

from src.modules.project.application.web.schemas.get_project_schema import GetProjectResponseSchema

class GetAllProjectsResponseSchema(RootModel[list[GetProjectResponseSchema]]):
    pass