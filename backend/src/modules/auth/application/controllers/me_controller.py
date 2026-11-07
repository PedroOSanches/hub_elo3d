from src.modules.auth.domain.errors.auth_error_usecase import AuthUnathorizedAction
from src.modules.auth.application.usecases.me_usecase import MeUsecase
from src.modules.auth.application.web.schemas.me_responses import MeResponseSchema


class MeController:

    def __init__(self, usecase: MeUsecase) -> None:
        self.usecase = usecase

    def __call__(
            self,
            *,
            access_token: str | None
            ) -> MeResponseSchema:

        if access_token is None:
            raise AuthUnathorizedAction()
        
        return self.usecase(access_token=access_token)
