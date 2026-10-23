from fastapi import Request
from fastapi.responses import JSONResponse

from src.shared.errors.base_error import BaseError
from src.shared.web.error_mapping import get_status_code


async def base_error_handler(
        request: Request,
        exc: BaseError,
) -> JSONResponse:
    return JSONResponse(
        status_code=get_status_code(exc),
        content={'message': exc.message}
    )