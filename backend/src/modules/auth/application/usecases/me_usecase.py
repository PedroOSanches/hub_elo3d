from pydantic import BaseModel
from src.modules.auth.infra.security.jwt_service import JWTService
from src.modules.auth.application.web.schemas.me_responses import MeResponseSchema
from src.modules.auth.infra.external.gateways.gateway_user import GatewayUser
from src.shared.errors.usecase_error import ForbiddenAction


class MeUsecase:

    def __init__(
            self,
            *,
            jwt_service: JWTService,
            ) -> None:
        self.jwt_service = jwt_service


    def __call__(
            self, 
            access_token: str
            ) -> MeResponseSchema:

        try:
            payload = self.jwt_service.decode_token(token=access_token)

            return MeResponseSchema(
                user_id=payload.get('sub'), # type: ignore
                role=payload.get('role') # type: ignore
            )
        except:
            raise ForbiddenAction('because token is invalid')