import logging

from fastapi import APIRouter, Header, Body, status

from business_logic.authentication import Authentication
from business_logic.websockets import WebSockets
from schemas.others.websockets import WSMessageIn, WSMessageOut

logger = logging.getLogger(__name__)

router = APIRouter()
AuthHandler = Authentication()
WSHandler = WebSockets()

@router.post(
    "/publish/",
    status_code=status.HTTP_200_OK,
    response_model=WSMessageOut,
)
def ws_send_message_endpoint(
    bearer: str = Header(
        ..., description="Custom `access_token` value", convert_underscores=False
    ),
    message_in: WSMessageIn = Body(
        ...,
        description="Message to send via WS to connected users"
    ),
)-> WSMessageOut:
    """
    *Send message to all connected users via WS server*
    """
    email = AuthHandler.get_email_by_access_token(access_token=bearer)
    logger.info(f":: websockets invocation from {email} ::")
    return WSHandler.ws_send_message(message=message_in.message)
