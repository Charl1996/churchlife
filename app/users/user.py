from sqlalchemy.orm import Session
from app.database.operations import (
    insert,
)
from app.database import User as DBUser
from app.users.user_schema import UserCreate, User


def create_user(db: Session, user: UserCreate) -> User:
    data_model = DBUser(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        organisation_id=user.organisation_id,
        password=user.password,
    )
    result = insert(db, data_model)
    # Send back schema user?
    return result


# def get_user_by_id(db: Session, user_id: int):
#     pass
#
#
# def get_user_by_email(db: Session, email: str):
#     pass
#
#
# def get_all_users(db: Session):
#     pass

