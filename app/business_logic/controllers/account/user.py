from uuid import UUID, uuid4
from datetime import date
from schemas.account.user import CreateUser, UpdateUser, User
from common.constants import EMAIL


# TODO: Connect with database

def create_user(create_user_cmd: CreateUser) -> User:
    return User(
        id=uuid4(),
        email=create_user_cmd.email,
        first_name=create_user_cmd.first_name,
        last_name=create_user_cmd.last_name,
        phone=create_user_cmd.phone,
        birthdate=date.today(),
        document_number="72182342",
    )


def get_user(user_id: UUID) -> User:
    return User(
        id=user_id,
        email=EMAIL,
        first_name="Collapse",
        last_name="Miracle",
        phone="923441233",
        birthdate=date.today(),
        document_number="72182342",
    )


def update_user(update_user_cmd: UpdateUser) -> User:
    return User(
        id=update_user_cmd.edit_user.id,
        email=EMAIL,
        first_name="Collapse",
        last_name="Miracle",
        phone="923441233",
        birthdate=date.today(),
        document_number="72182342",
    )
