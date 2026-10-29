from fastapi import FastAPI, APIRouter
from starlette.types import ExceptionHandler
from typing import cast


from src.shared.errors.base_error import BaseError
from src.shared.web.error_handlers import base_error_handler

from src.modules.user.application.web.routes.index import user_router
from src.modules.auth.application.web.routes.index import auth_router
from src.modules.auth.infra.middlewares.auth_middleware import AuthenticationMiddleware
from src.shared.environments import env

app = FastAPI()

app.add_middleware(
    AuthenticationMiddleware,
    jwt_secret=env.jwt_secret
)

app.add_exception_handler(
    BaseError,
    cast(ExceptionHandler, base_error_handler),
)

api_router = APIRouter(prefix='/api')

api_router.include_router(user_router, prefix='/user', tags=['User'])
api_router.include_router(auth_router, prefix='/auth', tags=['Auth'])

app.include_router(api_router)