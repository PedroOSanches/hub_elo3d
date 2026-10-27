from fastapi import APIRouter, Depends

from src.modules.auth.application.web.schemas.auth_schema import AuthRequestSchema

from src.modules.auth.application.web.schemas.auth_response_schema import AuthResponseSchema
from src.modules.auth.application.usecases.auth_usecase import AuthUsecase
from src.modules.auth.application.controllers.auth_controller import AuthController
from src.modules.auth.infra.external.gateways.gateway_user import GatewayUser


auth_router = APIRouter()

def get_login_depends():
    gateway = GatewayUser(GatewayUser.get_repo_user())
    usecase = AuthUsecase(gateway=gateway)
    return AuthController(usecase)

@auth_router.post(
    '/auth',
    response_class=AuthResponseSchema
)
def auth(
    request: AuthRequestSchema,
    controller: AuthController = Depends(get_login_depends)
    ):
    return controller(request)