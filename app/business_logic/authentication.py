import logging
from typing import Generator

from config import aws_settings
from exceptions import (
    WDSCognitoChangeResponse,
    WDSCognitoInternalError,
    WDSCognitoInvalidParameter,
    WDSCognitoNotAuthorized,
    WDSCognitoPasswordResetRequired,
    WDSCognitoResourceNotFound,
    WDSCognitoTooManyRequest,
    WDSCognitoUseNotConfirmed,
    WDSCognitoUserNotFound,
)
from external_services.cognito import client_cognito

logger = logging.getLogger(__name__)


class Authentication:
    def __init__(self):
        super().__init__()

    def get_email_by_access_token(self, access_token: str) -> str:
        """
        🤔🤔👀👀😎😎
        Gets the email of the user related with the given access_token
        """
        CognitoException = client_cognito.exceptions
        try:
            response = client_cognito.get_user(AccessToken=access_token)
            if not isinstance(response, dict):
                raise WDSCognitoChangeResponse  # pragma: no cover
            user_attribute_list = response.get("UserAttributes", [])
            if not user_attribute_list:
                raise WDSCognitoChangeResponse  # pragma: no cover
            for attribute in user_attribute_list:
                if "Name" not in attribute:
                    continue  # pragma: no cover
                if attribute.get("Name", "") == "email":
                    if "Value" not in attribute:
                        continue  # pragma: no cover
                    return attribute["Value"]
            raise WDSCognitoChangeResponse  # pragma: no cover
        except CognitoException.ResourceNotFoundException:  # pragma: no cover
            raise WDSCognitoResourceNotFound
        except CognitoException.InvalidParameterException:  # pragma: no cover
            raise WDSCognitoInvalidParameter
        except CognitoException.NotAuthorizedException:  # pragma: no cover
            raise WDSCognitoNotAuthorized
        except CognitoException.TooManyRequestsException:  # pragma: no cover
            raise WDSCognitoTooManyRequest
        except CognitoException.PasswordResetRequiredException:  # pragma: no cover
            raise WDSCognitoPasswordResetRequired
        except CognitoException.UserNotFoundException:  # pragma: no cover
            raise WDSCognitoUserNotFound
        except CognitoException.UserNotConfirmedException:  # pragma: no cover
            raise WDSCognitoUseNotConfirmed
        except CognitoException.InternalErrorException:  # pragma: no cover
            raise WDSCognitoInternalError


    def get_all_user_emails(self) -> Generator[str, None, None]:  # pragma: no cover
        paginator = client_cognito.get_paginator("list_users")
        for page in paginator.paginate(UserPoolId=aws_settings.COGNITO_USER_POOL_ID):
            for user in page["Users"]:
                for attribute in user["Attributes"]:
                    if attribute["Name"] == "email":
                        yield attribute["Value"]
        return

    def delete_all_users(self):  # pragma: no cover
        for email in self.get_all_user_emails():
            self.admin_delete_user(email)
