from fastapi import FastAPI
from starlette.types import ExceptionHandler
from typing import cast


from src.shared.errors.base_error import BaseError
from src.shared.web.error_handlers import base_error_handler
from src.modules.printers.application.web.routes.index import router as printers_router

app = FastAPI()

app.add_exception_handler(
    BaseError,
    base_error_handler,
)

app.include_router(printers_router, prefix="/printers", tags=["Printers"])
