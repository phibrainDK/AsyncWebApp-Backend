from fastapi import APIRouter

from api.routes.account import router as account
from api.routes.files import router as files

router = APIRouter()

router.include_router(
    account.router,
    prefix="/account",
    tags=["Account"],
)

router.include_router(
    files.router,
    prefix="/files",
    tags=["Files"],
)