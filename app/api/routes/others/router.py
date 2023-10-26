from fastapi import APIRouter

from api.routes.others import websockets

router = APIRouter()

router.include_router(
    websockets.router,
    prefix="/message",
)

