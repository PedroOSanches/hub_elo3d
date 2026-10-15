from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


from src.shared.errors.base_error import BaseError
from src.shared.web.error_handlers import base_error_handler

app = FastAPI()

app.add_exception_handler(
    BaseError,
    base_error_handler,
)