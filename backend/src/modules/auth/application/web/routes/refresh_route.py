from fastapi import APIRouter, Cookie, Depends, Response

from src.modules.auth.application.web.schemas.refresh_token_response_schema import RefreshTokenResponseSchema
from src.modules.auth.application.controllers.refresh_token_controller import RefreshTokenController
from src.modules.auth.application.usecases.refresh_token_usecase import RefreshTokenUsecase
from src.modules.auth.infra.external.gateways.gateway_user import GatewayUser
from src.modules.auth.infra.security.jwt_service import JWTService
from src.shared.environments import env

def get_refresh_token_controller():
    gateway = GatewayUser(GatewayUser.get_repo_user())
    usecase = RefreshTokenUsecase(
        gateway_user=gateway, 
        jwt_service=JWTService(jwt_secret=env.jwt_secret),
    )
    return RefreshTokenController(usecase=usecase)


refresh_router = APIRouter()

@refresh_router.post('/refresh')
def refresh_token(
    response: Response,
    refresh_token: str | None = Cookie(default=None),
    controller: RefreshTokenController = Depends(get_refresh_token_controller)
    ):

    access_token = controller(refresh_token=refresh_token)

    response.set_cookie(
        key='access_token',
        value=access_token.access_token,
        httponly=True,
        secure=False,
        samesite='lax',
        max_age= 15 * 60,
        path='/'
    )

    return {
        'message': 'New access_token created'
    }