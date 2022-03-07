from sqlalchemy.orm import Session
from app.models import User
from app.models.crud.decorators import insert
from app.models.schemas.user import UserCreate


@insert
def create_organisation(user: UserCreate):
    return User(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        organisation_id=user.organisation_id,
        password=user.password,
    )


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
