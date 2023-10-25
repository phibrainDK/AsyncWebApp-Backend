import logging
from datetime import datetime, timedelta

from botocore.exceptions import ClientError
from django.utils.http import http_date

from common.enums import ContentType
from config import aws_settings
from exceptions import AccessClientError
from external_services.s3 import client_s3
from schemas.files import PresignedUrlDownload, PresignedUrlUpload

logger = logging.getLogger(__name__)


class Storage:
    def __init__(self):
        super().__init__()

    def upload_files(self, object_name: str, content_type: ContentType) -> PresignedUrlUpload:
        expiration = http_date((datetime.utcnow() + timedelta(days=30)).timestamp())
        try:
            response = client_s3.generate_presigned_post(
                aws_settings.BACKEND_BUCKET_NAME,
                object_name,
                Fields={"Expires": expiration, "Content-Type": content_type.value},
                Conditions=[
                    ["starts-with", "$Content-Type", ""],
                    {"Expires": expiration},
                ],
                ExpiresIn=300,
            )
            return response
        except ClientError as e:  # pragma: no cover
            logger.info(f":: error as :: {str(e)}")
            raise AccessClientError from e

    def download_files(self, object_name: str) -> PresignedUrlDownload:
        logger.info(f":: S3 :: object_name = {object_name}")
        try:
            response = client_s3.generate_presigned_url(
                "get_object",
                Params={
                    "Bucket": aws_settings.BACKEND_BUCKET_NAME,
                    "Key": object_name,
                },
                ExpiresIn=300,
                HttpMethod="GET",
            )
            return PresignedUrlDownload(url=response)
        except ClientError as e:  # pragma: no cover
            logger.info(f":: error as :: {str(e)}")
            raise AccessClientError from e
