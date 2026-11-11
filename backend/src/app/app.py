import os

from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from starlette.types import ExceptionHandler
from typing import cast

from src.shared.errors.base_error import BaseError
from src.shared.web.error_handlers import base_error_handler
from src.modules.auth.infra.middlewares.auth_middleware import AuthenticationMiddleware
from src.shared.environments.environments import env

from src.app.easter_egg import teapot
from src.modules.user.application.web.routes.index import user_router
from src.modules.auth.application.web.routes.index import auth_router
from src.modules.project.application.web.routes.index import project_router
from src.modules.printers.application.web.routes.index import router as printers_router
from src.shared.environments.neo4j_connection_factory import connection


app = FastAPI()

frontend_origins = [
    origin.strip()
    for origin in os.getenv(
        "FRONTEND_ORIGINS",
        "http://localhost:3000, http://127.0.0.1:3000",
    ).split(",")
    if origin.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=frontend_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    AuthenticationMiddleware,
    jwt_secret=env.jwt_secret
)

app.add_exception_handler(
    BaseError,
    cast(ExceptionHandler, base_error_handler),
)

api_router = APIRouter(prefix="/api")

api_router.include_router(
    user_router,
    prefix="/user",
    tags=["User"]
)

api_router.include_router(user_router, prefix='/user', tags=['User'])
api_router.include_router(auth_router, prefix='/auth', tags=['Auth'])
api_router.include_router(printers_router, prefix='/printer', tags=['Printer'])
api_router.include_router(project_router, prefix="/projects", tags=["Projects"])
api_router.include_router(teapot)
app.include_router(api_router)

connection.close()