import logging
from typing import Optional

logger = logging.getLogger(__name__)


class AwsLambdaClient:
    def __init__(self):
        super().__init__()

    def invoke(
        self, 
        FunctionName: str, 
        InvocationType: str, 
        Payload: bytes,
        LogType: Optional[str], 
    ):
        class MockInvoke:
            class read:
                def decode(self, encoding: str):
                    response_payload = b'{"body": "Message sent to all clients."}'
                    payload_str = response_payload.decode('utf-8')
                    return payload_str

        return {
            "StatusCode": 200,
            "Payload": MockInvoke(),
        }


    class exceptions(Exception):  # pragma: no cover
        def ResourceNotFoundException(self):
            ...

        def InvocationException(self):
            ...
