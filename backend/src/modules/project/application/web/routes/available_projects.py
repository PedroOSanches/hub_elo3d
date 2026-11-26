from fastapi import APIRouter, Depends, Request, status

from src.modules.project.application.controllers.available_projects_controller import (
    AvailableProjectsController,
)
from src.modules.project.application.usecases.available_projects_usecase import (
    AvailableProjectsUsecase,
)
from src.modules.project.application.web.dependencies import (
    get_repo_project,
)
from src.modules.project.application.web.schemas.available_project_schema import (
    AvailableProjectsResponseSchema,
)

available_projects_route = APIRouter()

def get_available_projects() -> AvailableProjectsController:
    repo = get_repo_project()
    usecase = AvailableProjectsUsecase(repo=repo)
    return AvailableProjectsController(usecase=usecase)


@available_projects_route.get(
        path="/available_projects", 
        status_code=status.HTTP_200_OK, 
        response_model=AvailableProjectsResponseSchema
        )
async def available_projects(
    request: Request,
    controller: AvailableProjectsController = Depends(get_available_projects)
) -> AvailableProjectsResponseSchema:

    user_id = request.state.current_user.get('user_id')

    return controller(user_id=user_id)