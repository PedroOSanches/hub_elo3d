from fastapi import APIRouter
from .create_user import create_router

router = APIRouter()


router.include_router(router=create_router)