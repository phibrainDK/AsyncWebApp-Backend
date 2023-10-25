from uuid import uuid4

from fastapi import APIRouter, Header, Query, status

from business_logic.authentication import Authentication
from business_logic.files import Storage
from common.enums import ContentType, FileType
from schemas.files import PresignedUrlUpload

router = APIRouter()
AuthHandler = Authentication()
S3Handler = Storage()


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=PresignedUrlUpload,
)
def url_for_upload_endpoint(
    bearer: str = Header(
        ..., description="Custom `access_token` value", convert_underscores=False
    ),
    file_type: FileType = Query(
        ...,
        description="The `document type` that will be used by the backend "
        "to define the object key prefix",
        example=FileType.ACCOUNT,
    ),
    content_type: ContentType = Query(
        ...,
        description="The `content type` of the document to be uploaded",
        example=ContentType.PNG,
    ),
) -> PresignedUrlUpload:
    """
    *Generates presigned url for upload*
    """
    email = AuthHandler.get_email_by_access_token(access_token=bearer)
    return S3Handler.upload_files(
        object_name=f"{file_type.value}/{email}/{uuid4()}/${{filename}}",
        content_type=content_type,
    )