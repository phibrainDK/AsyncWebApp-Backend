import logging
from typing import Any, Dict, List

from schemas.files import PresignedField, PresignedUrlDownload, PresignedUrlUpload

logger = logging.getLogger(__name__)


class AwsS3Client:
    def __init__(self):
        super().__init__()

    def generate_presigned_url(
        self,
        method: Any,
        Params: Dict[str, Any],
        ExpiresIn: int,
        HttpMethod: str,
        **kwargs
    ) -> str:
        base_url = "https://upload.wikimedia.org/wikipedia/"
        file_url = "commons/thumb/5/52/Document-passed.svg/1973px-Document-passed.svg.png"
        return f"{base_url}{file_url}"
    

    def generate_presigned_post(
        self,
        bucket_name: Any,
        object_name: Any,
        Fields: Dict[str, Any],
        Conditions: List[Any],
        ExpiresIn: int,
        
    ) -> PresignedUrlUpload:
        return PresignedUrlUpload(
            url=object_name,
            fields=PresignedField(
                **{
                    "AWSAccessKeyId": "mock-6d7c-4352-968c-7fb62504631a",
                    "x-amz-security-token": "sec-token-6d7c-4352-968c-7fb62504631a",
                    "Content-Type": "application/pdf",
                    "Expires": "2050-08-06",
                    "key": "key-6d7c-4352-968c-7fb62504631a",
                    "signature": "sign-6d7c-4352-968c-7fb62504631a",
                    "policy": "policy-6d7c-4352-968c-7fb62504631a",
                }
            ),
        )