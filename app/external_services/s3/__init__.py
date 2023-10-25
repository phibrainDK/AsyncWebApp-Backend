from typing import Any

from common.enums import StageOption
from config import settings

if settings.ENV_STAGE in [StageOption.LOCAL, StageOption.TEST]:
    from external_services.s3.main import AwsS3Client

    client_s3: Any = AwsS3Client()
else:  # pragma: no cover
    import boto3

    client_s3: Any = boto3.client(service_name="s3")
