import logging

from fastapi import APIRouter, Header, Body, status

from business_logic.authentication import Authentication
from business_logic.websockets import WebSockets
from schemas.others.websockets import WSMessageAllIn, WSMessageAllOut, WSMessageOnlyIn, WSMessageOnlyOut

logger = logging.getLogger(__name__)

router = APIRouter()
AuthHandler = Authentication()
WSHandler = WebSockets()

@router.post(
    "/publish/all",
    status_code=status.HTTP_200_OK,
    response_model=WSMessageAllOut,
)
def ws_send_message_endpoint(
    bearer: str = Header(
        ..., description="Custom `access_token` value", convert_underscores=False
    ),
    message_all_in: WSMessageAllIn = Body(
        ...,
        description="Message to send via WS to connected users"
    ),
)-> WSMessageAllOut:
    """
    *Send message to all connected users via WS server*
    """
    email = AuthHandler.get_email_by_access_token(access_token=bearer)
    logger.info(f":: websockets invocation from {email} ::")
    return WSHandler.ws_send_message_all(message=message_all_in.message)


@router.post(
    "/publish/only",
    status_code=status.HTTP_200_OK,
    response_model=WSMessageOnlyOut,
)
def ws_send_message_endpoint(
    bearer: str = Header(
        ..., description="Custom `access_token` value", convert_underscores=False
    ),
    message_only_in: WSMessageOnlyIn = Body(
        ...,
        description="Message to send via WS to connected users"
    ),
)-> WSMessageOnlyOut:
    """
    *Send message to all connected users via WS server*
    """
    email = AuthHandler.get_email_by_access_token(access_token=bearer)
    logger.info(f":: websockets invocation from {email} ::")
    return WSHandler.ws_send_message_only(message=message_only_in.message, user_id=message_only_in.user_id)
