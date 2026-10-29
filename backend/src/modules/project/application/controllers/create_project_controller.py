
from src.modules.project.application.usecases.create_project_usecase import CreateProjectUsecase
from src.modules.project.application.web.schemas.create_project_schema import (CreateProjectRequestSchema, CreateProjectResponseSchema)

class CreateProjectController:
    def __init__(self, usecase: CreateProjectUsecase):
        self.usecase = usecase

    def __call__(self, request: CreateProjectRequestSchema) -> dict:
        project = self.usecase(
            title=request.title,
            date_end=request.date_end,
            pieces_quantity=request.pieces_quantity,
            category=request.category,
            description=request.description,
            urgency=request.urgency,
            filament_id=request.filament_id,
            files=request.files,
            technical_info=request.technical_info,
        )

        return CreateProjectResponseSchema.model_validate(project).model_dump(mode="json")