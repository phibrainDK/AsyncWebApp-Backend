from fastapi import APIRouter

from api.routes.files import download, upload

router = APIRouter()


router.include_router(
    download.router,
    prefix="/presigned-download-url",
)

router.include_router(
    upload.router,
    prefix="/presigned-upload-url",
)
