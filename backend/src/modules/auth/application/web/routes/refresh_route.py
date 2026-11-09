from fastapi import APIRouter, Cookie, Depends, Response

from src.modules.auth.application.web.schemas.refresh_token_response_schema import RefreshTokenResponseSchema
from src.modules.auth.application.controllers.refresh_token_controller import RefreshTokenController
from src.modules.auth.application.usecases.refresh_token_usecase import RefreshTokenUsecase
from src.modules.auth.infra.external.gateways.gateway_user import GatewayUser
from src.modules.auth.infra.security.jwt_service import JWTService
from src.shared.environments.environments import env

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

    tokens = controller(refresh_token=refresh_token)

    response.set_cookie(
        key='access_token',
        value=tokens.access_token,
        httponly=True,
        secure=False,
        samesite='lax',
        max_age= 15 * 60,
        path='/'
    )

    response.set_cookie(
        key="refresh_token",
        value=tokens.refresh_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=7 * 24 * 60 * 60,
        path="/api/auth",
    )
    
    return {
        'message': 'New tokens created'
    }