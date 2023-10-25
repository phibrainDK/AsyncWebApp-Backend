from dataclasses import dataclass
from datetime import date
from typing import Iterable, Optional
from uuid import UUID

from pydantic import BaseModel as _BaseModel
from pydantic import EmailStr, Field

from common.enums import OrderOption


class CustomBaseModel(_BaseModel):
    @classmethod
    def from_orms(cls, orm_objects: Iterable):
        """
        Converts each of the ORM Django objects from the iterable into their respective
        Pydantic schema (FastAPI -> Pydantic)
        """
        return [cls.from_orm(orm_object) for orm_object in orm_objects]


class User(CustomBaseModel):
    id: UUID
    email: EmailStr
    first_name: str
    last_name: str
    phone: Optional[str]
    birthdate: Optional[date]
    document_number: Optional[str]
    document_photo: Optional[str]
    profile_photo: Optional[str]

    class Config:
        orm_mode = True


@dataclass
class Pagination:
    order: OrderOption = Field(..., description="Order status")
    page: int = Field(..., description="The number of page")
    page_size: int = Field(..., description="Size of each page")


@dataclass
class CreateUser:
    email: EmailStr = Field(..., description="Email of the given user")
    first_name: str = Field(..., description="First name of the given user")
    last_name: str = Field(..., description="Last name of the given user")
    phone: str = Field(..., description="Contact number of the given user")


@dataclass
class UpdateUserSchema:
    birthdate: Optional[date] = None
    document_number: Optional[str] = ""     
    document_photo: Optional[str] = ""
    profile_photo: Optional[str] = ""


@dataclass
class EditUser:
    id: Optional[UUID] = Field(None, description="ID of the given user")
    birthdate: Optional[date] = Field(
        None, description="Birthdate of the given user to be updated"
    )
    document_number: Optional[str] = Field(
        "", description="Document number to be update"
    )
    document_photo: Optional[str] = Field(
        "", description="Document photo to be updated"
    )
    profile_photo: Optional[str] = Field("", description="Profile photo to be updated")


@dataclass
class UpdateUser:
    edit_user: EditUser

    def __init__(self, id: UUID, cmd: UpdateUserSchema):
        new_edit_user = EditUser()
        new_edit_user.id = id
        new_edit_user.birthdate = cmd.birthdate
        new_edit_user.document_number = cmd.document_number
        new_edit_user.document_photo = cmd.document_photo
        new_edit_user.profile_photo = cmd.profile_photo
        self.edit_user = new_edit_user
