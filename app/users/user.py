from sqlalchemy.orm import Session
from app.utils import hash_string
from app.database.operations import CRUDOperations

from app.database import User as UserModel
from app.users.user_schema import UserCreate, User


class UserHandler(CRUDOperations):

    @classmethod
    def get_database_model(cls):
        return UserModel

    @classmethod
    def get_schema_model(cls):
        return User

    @classmethod
    def create(cls, db: Session, user: UserCreate):
        user_model = UserModel(
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            password=hash_string(user.password),
        )
        user_model = cls.commit_to_db(db=db, model=user_model)
        return cls.get_schema_model().from_orm(user_model)
