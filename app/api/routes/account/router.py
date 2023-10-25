from fastapi import APIRouter

from api.routes.account import user

router = APIRouter()

router.include_router(
    user.router,
    prefix="/user",
)
