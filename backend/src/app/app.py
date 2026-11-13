import os

from contextlib import asynccontextmanager
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from starlette.types import ExceptionHandler
from typing import cast

from src.shared.errors.base_error import BaseError
from src.shared.web.error_handlers import base_error_handler
from src.modules.auth.infra.middlewares.auth_middleware import AuthenticationMiddleware
from src.shared.environments.environments import env
from src.shared.environments.neo4j_connection_factory import connection
from src.app.router import api_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        yield
    finally:
        connection.close()


app = FastAPI(lifespan=lifespan)




app.add_middleware(
    AuthenticationMiddleware,
    jwt_secret=env.jwt_secret
)

app.include_router(api_router)

app.add_exception_handler(
    BaseError,
    cast(ExceptionHandler, base_error_handler),
)

frontend_origins = env.frontend_origin

app = CORSMiddleware(
    app=app,
    allow_origins=frontend_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
