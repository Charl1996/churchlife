from sqlalchemy.orm import Session
from app.utils import hash_string
from app.database.interface import DatabaseInterface

from app.database import User as UserModel
from app.users.user_schema import (
    UserCreate,
    User as UserSchema,
)


class User(DatabaseInterface):

    # Make sure all these db_session's are closed after each request
    db_session: Session
    user: UserSchema

    @classmethod
    def database_model(cls):
        return UserModel

    @classmethod
    def schema_model(cls):
        return UserSchema

    @classmethod
    def create(cls, db_session: Session, data: dict):
        user_create = UserCreate(**data)

        user_model = UserModel(
            first_name=user_create.first_name,
            last_name=user_create.last_name,
            email=user_create.email,
            password=hash_string(user_create.password),
        )
        user_schema = super().create(db_session=db_session, model_data=user_model)
        return cls(db_session=db_session, user=user_schema)

    @classmethod
    def get(cls, db_session: Session, user_id: int):
        user_schema = super().get(db_session=db_session, model_id=user_id)
        return cls(db_session=db_session, user=user_schema)

    @classmethod
    def delete(cls, db_session: Session, user_id: int):
        # Do user specific stuff here
        # - Remove OrganisationUser
        super().delete(db_session=db_session, model_id=user_id)

    def __init__(self, db_session: Session, user: UserSchema):
        self.db_session = db_session
        self.user = user

    @property
    def fields(self) -> UserSchema:
        return self.user
