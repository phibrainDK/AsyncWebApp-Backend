import logging
import json

from config import aws_settings
from exceptions import LambdaResourceNotFoundException, LambdaInvocationException
from external_services.lambdas import client_lambda
from schemas.others.websockets import WSMessageAllOut, WSMessageOnlyOut


logger = logging.getLogger(__name__)

# TODO: Make it dynamically

WS_ENDPOINT = "w47tt670z9.execute-api.us-east-1.amazonaws.com/app-wds-ws-tf-wds-tf-wds"

class WebSockets:
    def __init__(self):
        super().__init__()

    def ws_send_message_all(self, message: str) -> WSMessageAllOut:
        event = {
            "type": "WS",
            "requestContext": {
                "eventType": "NOTIFY_ALL",
                "endpoint": WS_ENDPOINT,
                "customMessage": message,
            }
        }
        event_str = json.dumps(event)
        LambdaException = client_lambda.exceptions
        try:
            response = client_lambda.invoke(
                FunctionName=aws_settings.WEBSOCKETS_SERVER_NAME,
                InvocationType="RequestResponse",
                LogType="Tail",  # Optional
                Payload=event_str.encode('utf-8')
            )
            status_code = response['StatusCode']
            data_bytes = response['Payload'].read().decode('utf-8')
            data_json = json.loads(data_bytes)
            if data_json.get("body"):
                return WSMessageAllOut(
                    status_code=status_code,
                    message=data_json["body"],
                )
            else:
                return WSMessageAllOut(
                    status_code="422",
                    message="Hubo un error en el servidor de WS",
                )
        except LambdaException.ResourceNotFoundException:
            raise LambdaResourceNotFoundException
        except LambdaException.InvocationException:
            raise LambdaInvocationException
        except Exception as e:
            logger.info(":: General Exception Error ::", str(e))
            raise e
        
    def ws_send_message_only(self, message: str, user_id: str) -> WSMessageOnlyOut:
        event = {
            "type": "WS",
            "requestContext": {
                "eventType": "NOTIFY_ONLY",
                "endpoint": WS_ENDPOINT,
                "customMessage": message,
                "userId": user_id,
            }
        }
        event_str = json.dumps(event)
        LambdaException = client_lambda.exceptions
        try:
            response = client_lambda.invoke(
                FunctionName=aws_settings.WEBSOCKETS_SERVER_NAME,
                InvocationType="RequestResponse",
                LogType="Tail",  # Optional
                Payload=event_str.encode('utf-8')
            )
            status_code = response['StatusCode']
            data_bytes = response['Payload'].read().decode('utf-8')
            data_json = json.loads(data_bytes)
            if data_json.get("body"):
                return WSMessageAllOut(
                    status_code=status_code,
                    message=data_json["body"],
                )
            else:
                return WSMessageAllOut(
                    status_code="422",
                    message="Hubo un error en el servidor de WS",
                )
        except LambdaException.ResourceNotFoundException:
            raise LambdaResourceNotFoundException
        except LambdaException.InvocationException:
            raise LambdaInvocationException
        except Exception as e:
            logger.info(":: General Exception Error ::", str(e))
            raise e