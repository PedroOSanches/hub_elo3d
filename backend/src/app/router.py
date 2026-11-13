from fastapi import APIRouter
from src.app.easter_egg import teapot
from src.modules.user.application.web.routes.index import user_router
from src.modules.auth.application.web.routes.index import auth_router
from src.modules.project.application.web.routes.index import project_router
from src.modules.printers.application.web.routes.index import router as printers_router

api_router = APIRouter(prefix="/api")

api_router.include_router(user_router, prefix='/user', tags=['User'])
api_router.include_router(auth_router, prefix='/auth', tags=['Auth'])
api_router.include_router(printers_router, prefix='/printer', tags=['Printer'])
api_router.include_router(project_router, prefix="/projects", tags=["Projects"])
api_router.include_router(teapot)