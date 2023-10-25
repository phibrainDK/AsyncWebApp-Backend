import logging
from uuid import UUID

from fastapi import APIRouter, Body, Header, Path, status

from business_logic.authentication import Authentication
from business_logic.controllers.account.user import create_user, get_user, update_user
from schemas.account.user import CreateUser, UpdateUser, UpdateUserSchema, User

router = APIRouter()
AuthHandler = Authentication()
logger = logging.getLogger(__name__)


# TODO: Remove when cognito is working
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=User)
def create_user_endpoint(
    bearer: str = Header(
        ..., description="Custom `access_token` value", convert_underscores=False
    ),
    user_body_in: CreateUser = Body(..., description="User fields to create"),
):
    email = AuthHandler.get_email_by_access_token(access_token=bearer)
    logger.info(f":: create user from {email} ::")
    return create_user(create_user_cmd=user_body_in)


@router.get("/{user_id}/", status_code=status.HTTP_200_OK, response_model=User)
def get_user_endpoint(
    bearer: str = Header(
        ..., description="Custom `access_token` value", convert_underscores=False
    ),
    user_id: UUID = Path(..., title="user ID", description="ID of the given user")
):
    email = AuthHandler.get_email_by_access_token(access_token=bearer)
    logger.info(f":: get user from {email} ::")
    return get_user(user_id=user_id)


@router.patch(
    "/{user_id}/",
    status_code=status.HTTP_200_OK,
    response_model=User, 
)
def update_user_endpoint(
    bearer: str = Header(
        ..., description="Custom `access_token` value", convert_underscores=False
    ),
    user_id: UUID = Path(..., title="User ID", description="ID of the given user"),
    user_update_in: UpdateUserSchema = Body(
        ..., description="Private loan fields to update"
    ),
):
    email = AuthHandler.get_email_by_access_token(access_token=bearer)
    logger.info(f":: update user from {email} ::")
    update_user_cmd = UpdateUser(id=user_id, cmd=user_update_in)
    return update_user(update_user_cmd=update_user_cmd)
