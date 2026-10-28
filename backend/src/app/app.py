from fastapi import FastAPI, APIRouter
from starlette.types import ExceptionHandler
from typing import cast


from src.shared.errors.base_error import BaseError
from src.shared.web.error_handlers import base_error_handler

from src.modules.user.application.web.routes.index import user_router
from src.modules.auth.application.web.routes.index import auth_router

app = FastAPI()

app.add_exception_handler(
    BaseError,
    cast(ExceptionHandler, base_error_handler),
)

api_router = APIRouter(prefix='/api')

api_router.include_router(user_router, prefix='/user')
api_router.include_router(auth_router, prefix='/auth')

app.include_router(api_router)