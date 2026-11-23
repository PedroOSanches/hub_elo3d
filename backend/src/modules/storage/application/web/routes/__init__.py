from fastapi import APIRouter

from src.modules.storage.application.web.routes.generate_upload_url_route import (
    generate_upload_route,
)

upload_route = APIRouter()

upload_route.include_router(generate_upload_route)