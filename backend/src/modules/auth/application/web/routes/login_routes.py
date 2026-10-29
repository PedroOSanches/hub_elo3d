from fastapi import APIRouter, Depends, Response

from src.modules.auth.application.web.schemas.login_schema import LoginRequestSchema

from src.modules.auth.application.usecases.login_usecase import LoginUsecase
from src.modules.auth.application.controllers.login_controller import LoginController
from src.modules.auth.infra.external.gateways.gateway_user import GatewayUser
from src.modules.auth.infra.security.jwt_service import JWTService
from src.shared.environments import env

login_router = APIRouter()

def get_login_depends():
    jwt_service = JWTService(jwt_secret=env.jwt_secret)
    gateway = GatewayUser(GatewayUser.get_repo_user())
    usecase = LoginUsecase(gateway=gateway, jwt_service=jwt_service)
    return LoginController(usecase)

@login_router.post(
    '/login',
)
def login(
    request: LoginRequestSchema,
    response: Response,
    controller: LoginController = Depends(get_login_depends)
    ):

    tokens = controller(request)
    
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

    return {'message': 'Login realizado com sucesso'}