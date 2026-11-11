from fastapi import APIRouter
from fastapi.responses import FileResponse


teapot = APIRouter()


@teapot.get('/tea')
def teapot_route():
    return FileResponse(status_code=418, path='src/shared/web/easter_egg.webp', media_type='image/webp')