import logging

from fastapi import APIRouter, Header, Query, status

from business_logic.authentication import Authentication
from business_logic.files import Storage
from schemas.files import PresignedUrlDownload

logger = logging.getLogger(__name__)

router = APIRouter()
AuthHandler = Authentication()
S3Handler = Storage()

@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=PresignedUrlDownload,
)
def url_for_download_endpoint(
    bearer: str = Header(
        ..., description="Custom `access_token` value", convert_underscores=False
    ),
    object_name: str = Query(
        ...,
        description="Format: `{document-type}/{email}/{uuid}/{filename}`. "
        "Where the filename is set",
    ),
)-> PresignedUrlDownload:
    # TODO: Enhacement object_name via regex
    """
    *Generates presigned url to download*
    """
    email = AuthHandler.get_email_by_access_token(access_token=bearer)
    logger.info(f":: download from {email} via objects name = {object_name}::")
    return S3Handler.download_files(
        object_name=object_name,
    )
