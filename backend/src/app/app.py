from fastapi import FastAPI


from src.shared.errors.base_error import BaseError
from src.shared.web.error_handlers import base_error_handler

app = FastAPI()

app.add_exception_handler(
    BaseError,
    base_error_handler,
)