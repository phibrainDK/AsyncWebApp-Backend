from typing import Any

from common.enums import StageOption
from config import settings

if settings.ENV_STAGE in [StageOption.LOCAL, StageOption.TEST]:
    from external_services.lambdas.main import AwsLambdaClient

    client_lambda: Any = AwsLambdaClient()
else:  # pragma: no cover
    import boto3

    client_lambda: Any = boto3.client(
        service_name="lambda",
    )
