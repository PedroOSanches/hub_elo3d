from uuid import UUID

from fastapi import APIRouter, HTTPException, Request, status

from src.modules.user.application.web.dependencies import get_repo_user
from src.modules.user.application.web.schemas.user_response_schema import (
    UserResponseSchema,
)
from src.modules.user.domain.errors.user_usecase_errors import NoUsersFound


me_router = APIRouter()


@me_router.get("/me", status_code=status.HTTP_200_OK)
def get_authenticated_user(request: Request):
    current_user = getattr(request.state, "current_user", None)
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
        )

    try:
        user = get_repo_user().get_user(UUID(current_user["user_id"]))
    except (ValueError, NoUsersFound) as error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authenticated user was not found",
        ) from error

    return UserResponseSchema.model_validate(user).model_dump(mode="json")
