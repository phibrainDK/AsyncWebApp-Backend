from typing import Any

from common.enums import StageOption
from config import settings

if settings.ENV_STAGE in [StageOption.LOCAL, StageOption.TEST]:
    from external_services.cognito.main import AwsCognitoClient

    client_cognito: Any = AwsCognitoClient()
else:  # pragma: no cover
    import boto3

    client_cognito: Any = boto3.client(
        service_name="cognito-idp",
        region_name=settings.DEPLOY_REGION,
    )
