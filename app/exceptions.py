from typing import Optional

from common.enums import ModalType
from fastapi import status


class WDSException(Exception):
    # Default status_code for WDS Exceptions
    status_code: int = status.HTTP_422_UNPROCESSABLE_ENTITY
    modal_type: str = ModalType.GENERAL
    error_code: str
    error_message: str
    translated_error_message: Optional[str] = ""

    @property
    def detail(self):
        return {
            "error_code": self.error_code,
            "error_message": self.error_message,
            "status_code": self.status_code,
            "translated_error_message": self.translated_error_message,
            "modal_type": self.modal_type,
        }


class InvalidUserDocumentNumber(WDSException):
    status_code = status.HTTP_400_BAD_REQUEST
    error_code = "LEN001"
    error_message = (
        "The given related agency ruc of the user described by document number "
        "doesn't match (invalid dni user)"
    )

    def __init__(self, error_message: str, translated_error_message: str) -> None:
        self.error_message = error_message
        self.translated_error_message = translated_error_message


class ObjectAlreadyExist(WDSException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    error_code = "LEN002"
    error_message = "The given object is already found on the database"

    def __init__(self, error_message: str, translated_error_message: str) -> None:
        self.error_message = error_message
        self.translated_error_message = translated_error_message


class InvalidUpdate(WDSException):
    status_code = status.HTTP_409_CONFLICT
    error_code = "LEN003"
    error_message = "It is impossible to change fields required on the current object"

    def __init__(self, error_message: str, translated_error_message: str) -> None:
        self.error_message = error_message
        self.translated_error_message = translated_error_message


# =================================== COGNITO ========================================


class WDSCognitoChangeResponse(WDSException):
    status_code = status.HTTP_403_FORBIDDEN
    error_code = "COG000"
    error_message = "Amazon Cognito changed the way of sending the response"


class WDSCognitoResourceNotFound(WDSException):
    status_code = status.HTTP_403_FORBIDDEN
    error_code = "COG001"
    error_message = "Amazon Cognito service can't find the requested resource"


class WDSCognitoInvalidParameter(WDSException):
    status_code = status.HTTP_403_FORBIDDEN
    error_code = "COG002"
    error_message = "Amazon Cognito service encountered an invalid parameter"


class WDSCognitoNotAuthorized(WDSException):
    status_code = status.HTTP_403_FORBIDDEN
    error_code = "COG003"
    error_message = "The given user isn't authorized"
    translated_error_message = (
        "El usuario no esta autorizado para realizar esta operación."
    )


class WDSCognitoTooManyRequest(WDSException):
    status_code = status.HTTP_403_FORBIDDEN
    error_code = "COG004"
    error_message = "The given user has made too many requests for a given operation"


class WDSCognitoPasswordResetRequired(WDSException):
    status_code = status.HTTP_403_FORBIDDEN
    error_code = "COG005"
    error_message = "Password reset is required"


class WDSCognitoUserNotFound(WDSException):
    status_code = status.HTTP_403_FORBIDDEN
    error_code = "COG006"
    error_message = "The given user isn't found"


class WDSCognitoUseNotConfirmed(WDSException):
    status_code = status.HTTP_403_FORBIDDEN
    error_code = "COG007"
    error_message = "The given user isn't confirmed successfully"


class WDSCognitoInternalError(WDSException):
    status_code = status.HTTP_403_FORBIDDEN
    error_code = "COG008"
    error_message = "Amazon Cognito encountered an internal error"


class WDSCognitoTokenNotFound(WDSException):
    status_code = status.HTTP_403_FORBIDDEN
    error_code = "COG009"
    error_message = "Can't found the token in cognito response"


class WDSCognitoUnexpectedLambdaException(WDSException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    error_code = "COG010"
    error_message = (
        "Amazon Cognito service encounters an unexpected "
        "exception with the Lambda service"
    )


class WDSCognitoInvalidUserPoolConfiguration(WDSException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    error_code = "COG011"
    error_message = "Invalid user pool configuration in Amazon Cognito"


class WDSCognitoUserLambdaValidationException(WDSException):
    status_code = status.HTTP_403_FORBIDDEN
    error_code = "COG012"
    error_message = (
        "Amazon Cognito service encounters a user validation exception "
        "with the Lambda service"
    )


class WDSCognitoInvalidLambdaResponse(WDSException):
    status_code = status.HTTP_403_FORBIDDEN
    error_code = "COG013"
    error_message = "Amazon Cognito service encounters an invalid Lambda response"


class WDSCognitoMFAMethodNotFound(WDSException):
    status_code = status.HTTP_404_NOT_FOUND
    error_code = "COG014"
    error_message = (
        "Amazon Cognito cannot find a multi-factor authentication (MFA) method"
    )


class WDSCognitoInvalidSmsRoleAccessPolicy(WDSException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    error_code = "COG015"
    error_message = (
        "role provided for SMS configuration does not have permission "
        "to publish using Amazon SNS"
    )


class WDSCognitoInvalidSmsRoleTrustRelationship(WDSException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    error_code = "COG016"
    error_message = (
        "trust relationship is not valid for the role provided for SMS configuration"
    )


class WDSCognitoUsernameExistsException(WDSException):
    status_code = status.HTTP_403_FORBIDDEN
    error_code = "COG017"
    error_message = "the username provided already exists in Amazon Cognito"


class WDSCognitoUserEmailAlreadyExists(WDSException):
    status_code = status.HTTP_403_FORBIDDEN
    error_code = "COG018"
    error_message = "The given email is already registered"
    translated_error_message = (
        "El email ya se encuentra registrado en alguno de nuestros "
        "sistemas de autenticación."
    )


class WDSLambdaSessionException(WDSException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    error_code = "LAM001"
    error_message = "Couldn't create a session from lambda AWS service"


class WDSLambdaAsyncException(WDSException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    error_code = "LAM002"
    error_message = (
        "An unexpected problem ocurred while calling async lambda AWS service"
    )
    translated_error_message = "Ha ocurrido un error en el sistema no esperados."

    def __init__(self, error_message: str) -> None:
        self.error_message = error_message  # pragma: no cover


class WDSLambdaMultipleRequestException(WDSException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    error_code = "LAM003"
    error_message = "Too many requests for AWS Lambda. Check limit quotas"
    translated_error_message = (
        "El sistema ha llegado al maximo de número de procesos concurrentes."
    )



class LambdaResourceNotFoundException(WDSException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    error_code = "LAM004"
    error_message = (
        "Not found resource lambda AWS service"
    )
    translated_error_message = ""

    def __init__(self, error_message: str) -> None:
        self.error_message = error_message


class LambdaInvocationException(WDSException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    error_code = "LAM005"
    error_message = (
        "Error while invocation lambda AWS service"
    )
    translated_error_message = ""

    def __init__(self, error_message: str) -> None:
        self.error_message = error_message



# ===================================== S3 Exceptions ==============================


class S3UploadFailed(WDSException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    error_code = "S3000"
    error_message = (
        "The file couldn't be uploaded to S3, check credentials configuration"
    )


class S3DownloadFailed(WDSException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    error_code = "S3001"
    error_message = (
        "The file couldn't be downloaded from S3, check credentials configuration"
    )


# ======================== File Exceptions ==========================================


class FileException(Exception):
    """Class to handle all file exceptions"""

    result_code: str
    message: str
    status_code: int

    @property
    def detail(self):
        return {
            "result_code": self.result_code,
            "message": self.message,
            "status_code": self.status_code,
        }  # pragma: no cover


class AccessClientError(FileException):
    """Exception raised when user not having permissions
    request download or upload of file"""

    result_code = "FILE001"
    message = "There are access problems from botocore using the endpoint"
    status_code = status.HTTP_401_UNAUTHORIZED
