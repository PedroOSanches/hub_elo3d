from typing import Any
from uuid import UUID

from src.modules.project.application.usecases.available_projects_usecase import (
    AvailableProjectsUsecase,
)
from src.shared.errors.controller_error import WrongTypeParameter

from ..web.schemas.available_project_schema import AvailableProjectsResponseSchema


class AvailableProjectsController:

    def __init__(self, usecase: AvailableProjectsUsecase) -> None:
        self.usecase = usecase

    def __call__(self, user_id: str) -> Any:
        try:
            user_id_uuid = UUID(user_id)
        except Exception as err:
            raise WrongTypeParameter(
                field_name='user_id',
                field_type_expected='UUID',
                field_type_received=user_id.__class__.__name__
            ) from err

        return AvailableProjectsResponseSchema.model_validate(
            self.usecase(user_id=user_id_uuid)
        )