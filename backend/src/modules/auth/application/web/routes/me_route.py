from fastapi import APIRouter, Depends, Response
from fastapi.requests import Request
from src.modules.auth.application.controllers.me_controller import MeController
from src.modules.auth.application.usecases.me_usecase import MeUsecase
from src.modules.auth.infra.security.jwt_service import JWTService
from src.shared.environments import env
from src.modules.auth.application.web.schemas.me_responses import MeResponseSchema
route_me = APIRouter()

def get_me_depends():
    jwt = JWTService(jwt_secret=env.jwt_secret)
    usecase = MeUsecase(jwt_service=JWTService(jwt_secret=env.jwt_secret))
    return MeController(usecase)

@route_me.get('/me', response_model=MeResponseSchema)
async def me(
    request: Request,
    controller: MeController = Depends(get_me_depends)
    ):

    access_token = request.cookies.get('access_token')

    return controller(access_token=access_token)