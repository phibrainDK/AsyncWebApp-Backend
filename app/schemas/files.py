from typing import Optional

from pydantic import BaseModel, Field

########################################################################################
#                                        PROCESS                                       #
########################################################################################


class PresignedField(BaseModel):
    aws_access_key_id: str = Field(alias="AWSAccessKeyId")
    x_amz_security_token: Optional[str] = Field(alias="x-amz-security-token")
    content_type: str = Field(alias="Content-Type")
    expires: str = Field(alias="Expires")
    key: str = Field(..., description="Key")
    signature: str = Field(..., description="Signature")
    policy: str = Field(..., description="Policy")


########################################################################################
#                                        INPUT                                         #
########################################################################################


########################################################################################
#                                        OUTPUT                                        #
########################################################################################


class PresignedUrlDownload(BaseModel):
    url: str = Field(..., description="Presigned url for downloading files from AWS S3")


class PresignedUrlUpload(BaseModel):
    url: str = Field(..., desciption="Presigned url for uploading files to AWS S3")
    fields: PresignedField
