import logging
from typing import Any, Dict, List

from common.constants import EMAIL


logger = logging.getLogger(__name__)


class AwsCognitoClient:
    def __init__(self):
        super().__init__()

    def get_user(self, AccessToken: str) -> Dict[str, Any]:
        # TODO: get the email from token to local env
        return {
            "UserAttributes": [
                {
                    "Name": "email",
                    "Value": EMAIL,
                }
            ]
        }


    def get_paginator(self, param: str):  # pragma: no cover
        class Paginator:
            def paginate(self, UserPoolId: str) -> List[Dict[str, Any]]:
                return [
                    {
                        "Users": [
                            {
                                "Attributes": [
                                    {
                                        "Name": "email",
                                        "Value": EMAIL,
                                    }
                                ]
                            }
                        ]
                    }
                ]

        return Paginator()


    class exceptions(Exception):  # pragma: no cover
        def ResourceNotFoundException(self):
            ...

        def InvalidParameterException(self):
            ...

        def NotAuthorizedException(self):
            ...

        def TooManyRequestsException(self):
            ...

        def PasswordResetRequiredException(self):
            ...

        def UserNotFoundException(self):
            ...

        def UserNotConfirmedException(self):
            ...

        def InternalErrorException(self):
            ...

        def UnexpectedLambdaException(self):
            ...

        def InvalidUserPoolConfigurationException(self):
            ...

        def UserLambdaValidationException(self):
            ...

        def InvalidLambdaResponseException(self):
            ...

        def MFAMethodNotFoundException(self):
            ...

        def InvalidSmsRoleAccessPolicyException(self):
            ...

        def InvalidSmsRoleTrustRelationshipException(self):
            ...

        def UsernameExistsException(self):
            ...
